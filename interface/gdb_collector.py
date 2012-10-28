# (void)walker application interface
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

import gdb

from arch.context import Context
from arch.context import ContextRegister
from arch.cpu import Register
from base.decorators import singleton
from interface.collector import CollectorFactory


@singleton
class GdbCollectorFactory(CollectorFactory):
    def create_register(self, name):
        class GdbRegister(Register):
            def __init__(self, name):
                super(GdbRegister, self).__init__(name)

            def size(self):
                size = gdb.parse_and_eval('sizeof($' + self.name() + ')')
                try:
                    return int(size)
                except gdb.error:
                    return None

            def value(self):
                value = gdb.parse_and_eval('$' + self.name())
                try:
                    return long(value)
                except gdb.error:
                    return None

        return GdbRegister(name)

    def create_context(self, cpu):
        class GdbContext(Context):
            def _update_registers(self):
                for name, register in self.cpu().registers():
                    self._registers[name] = ContextRegister(register)

            def _update_stack(self):
                result = gdb.execute(('x /%dxb $sp' %
                                      (0x8 * self._STACK_LINES)),
                                     False, True)

                for line in result.split('\n'):
                    if not line:
                        continue
                    match = Context._data_exp.search(line).groupdict()
                    address = int(match['address'], 16)
                    self._stack[address] = [int(i, 16)
                                            for i in match['data'].split()]

            def _update_instructions(self):
                result = gdb.execute(('x /%di $pc' % self._TOTAL_INSTRUCTIONS),
                                     False, True)
                for line in result.split('\n'):
                    line = line.replace('%', '%%')
                    instruction = self._instruction_exp.search(line)
                    if instruction:
                        self._instructions.append(instruction.groupdict())

            def __init__(self, cpu):
                super(GdbContext, self).__init__(cpu)

                self._update_registers()
                self._update_stack()
                self._update_instructions()

        return GdbContext(cpu)
