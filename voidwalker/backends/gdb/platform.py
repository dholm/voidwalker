# (void)walker GDB backend
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from ...framework.platform import Context
from ...framework.platform import CpuFactory
from ...framework.platform import PlatformFactory
from ...framework.platform import create_static_register
from ...framework.types import DataChunk

from ...application.parameters.context import ContextInstructionsParameter
from ...application.parameters.context import ContextStackParameter


class GdbCpuFactory(CpuFactory, object):
    def create_register(self, cpu, register):
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


class GdbPlatformFactory(PlatformFactory, object):
    def create_context(self, config, thread):
        stackdws = config.parameter(ContextStackParameter.name()).value()
        instrs_name = ContextInstructionsParameter.name()
        instructions = config.parameter(instrs_name).value()
        inferior = thread.get_inferior()

        class GdbContext(Context):
            def _update_registers(self):
                for group, register_dict in inferior.cpu().registers():
                    tuples = [(x.name(), create_static_register(x))
                              for x in register_dict.itervalues()]
                    register_dict = OrderedDict(tuples)
                    self._registers[group] = register_dict

            def _update_stack(self):
                size = stackdws * 0x8
                address = inferior.cpu().stack_pointer().value() & ~0xf
                stack = inferior.read_memory(address, size)
                self._stack = DataChunk(address, stack)

            def _update_instructions(self):
                address = inferior.cpu().program_counter().value()
                length = instructions
                listing = inferior.disassemble(address, length)
                self._instruction_listing = listing

            def __init__(self):
                cpu = inferior.cpu()
                program_counter = cpu.program_counter().name()
                super(GdbContext, self).__init__(program_counter)

                self._update_registers()
                self._update_stack()
                self._update_instructions()

        return GdbContext()
