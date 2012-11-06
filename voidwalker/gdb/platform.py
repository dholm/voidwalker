# (void)walker GDB backend
# Copyright (C) 2012 David Holm <dholmster@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import OrderedDict
import gdb
import re

from ..platform.context import Context
from ..platform.cpu import Instruction
from ..platform.cpu import create_static_register
from ..platform.factory import PlatformFactory
from ..types.data import DataChunk
from ..utils.decorators import singleton_implementation


@singleton_implementation(PlatformFactory)
class GdbPlatformFactory(object):
    def create_register(self, register):
        class GdbRegister(type(register), object):
            _value_exp = re.compile(r'(?P<variable>.+)\s*=\s*(?P<value>.+)')

            def __init__(self, name):
                super(GdbRegister, self).__init__(name)

            def size(self):
                size = gdb.parse_and_eval('sizeof($%s)' % register.name())
                try:
                    return int(size)
                except gdb.error:
                    return None

            def value(self):
                try:
                    result = gdb.execute('p /x $%s' % register.name(),
                                         to_string=True)
                    match = self._value_exp.search(result)

                    return abs(long(match.group('value'), 16))
                except ValueError:
                    return None
                except gdb.error:
                    return None

        return GdbRegister(register.name())

    def create_context(self, inferior, thread):
        class GdbContext(Context):
            _instruction_exp = re.compile((r'(?P<meta>\S+)?\s*'
                                           r'(?P<address>0x[0-9a-f]+){1}\s*'
                                           r'(?P<symbol><.+>){0,1}:\s*'
                                           r'(?P<mnemonic>\S+){1}\s*'
                                           r'(?P<operands>.+)?$'),
                                          re.IGNORECASE)

            def _update_registers(self):
                for group, register_dict in inferior.cpu().registers():
                    register_dict = OrderedDict((x.name(),
                                                 create_static_register(x))
                                                for x in
                                                register_dict.itervalues())
                    self._registers[group] = register_dict

            def _update_stack(self):
                size = self._param_stackdw() * 0x8
                address = abs(long(gdb.parse_and_eval('$sp'))) & ~0xf
                stack = inferior.read_memory(address, size)
                self._stack = DataChunk(address, stack)

            def _update_instructions(self):
                result = gdb.execute(('x /%di $pc' %
                                      (self._param_instructions() + 1)),
                                     to_string=True)
                parsed = []
                for line in result.split('\n'):
                    line = line.replace('%', '%%')
                    instruction = self._instruction_exp.search(line)
                    if instruction:
                        parsed.append(instruction.groupdict())

                for i in range(len(parsed) - 1):
                    size = (long(parsed[i + 1]['address'], 16) -
                            long(parsed[i]['address'], 16))
                    address = long(parsed[i]['address'], 16)
                    data = inferior.read_memory(address, size)

                    symbol = parsed[i]['symbol']
                    mnemonic = parsed[i]['mnemonic']
                    operands = parsed[i]['operands']
                    self._instructions[address] = Instruction(data, mnemonic,
                                                              operands, symbol)

            def __init__(self):
                cpu = inferior.cpu()
                instruction_pointer = cpu.instruction_pointer().name()
                super(GdbContext, self).__init__(instruction_pointer)

                self._update_registers()
                self._update_stack()
                self._update_instructions()

        return GdbContext()
