# (void)walker hardware platform support
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
import re
import string
from collections import OrderedDict

from cpu import Register

class ContextRegister(Register):
    _size = None
    _value = None

    def __init__(self, register):
        super(ContextRegister, self).__init__(register.name())
        self._size = register.size()
        self._value = register.value()

    def size(self):
        return self._size

    def value(self):
        return self._value


class Context(object):
    _TOTAL_INSTRUCTIONS = 6
    _STACK_LINES = 6

    _instruction_exp = re.compile((r'(?P<meta>\S+)?\s*'
                                   r'(?P<address>0x[0-9a-f]+){1}\s*'
                                   r'(?P<symbol><.+>){0,1}:\s*'
                                   r'(?P<mnemonic>\S+){1}\s*'
                                   r'(?P<operands>.+)?$'),
                                  re.MULTILINE | re.IGNORECASE)

    _data_exp = re.compile((r'(?:\s*(?P<address>0x[0-9a-f]+):\s*)'
                            r'(?P<data>(?:\s*0x[0-9a-f]+)+\s*)'),
                           re.IGNORECASE)

    _cpu = None
    _registers = None
    _instructions = None
    _stack = None

    def _update_registers(self):
        for name, register in self._cpu.registers():
            self._registers[name] = ContextRegister(register)

    def _update_stack(self):
        result = gdb.execute(('x /%dxb $sp' % (0x8 * self._STACK_LINES)),
                             False, True)

        for line in result.split('\n'):
            if not line:
                continue
            match = self._data_exp.search(line).groupdict()
            address = int(match['address'], 16)
            self._stack[address] = [int(i, 16) for i in match['data'].split()]


    def _update_instructions(self):
        result = gdb.execute(('x /%di $pc' % self._TOTAL_INSTRUCTIONS),
                             False, True)
        lines = self._instruction_exp.finditer(result)
        for instruction in lines:
            self._instructions.append(instruction.groupdict())


    def __init__(self, cpu):
        self._cpu = cpu

        self._registers = OrderedDict()
        self._stack = OrderedDict()
        self._instructions = []

        self._update_registers()
        self._update_stack()
        self._update_instructions()


    def cpu(self):
        return self._cpu

    def stack(self):
        return self._stack

    def register(self, name):
        if name not in self._registers:
            return None
        return self._registers[name]

    def registers(self):
        return self._registers.iteritems()

    def instructions(self):
        return iter(self._instructions)
