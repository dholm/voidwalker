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

import re
from collections import OrderedDict

from .cpu import Register


class ContextRegister(Register):
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
                                  re.IGNORECASE)

    _data_exp = re.compile((r'(?:\s*(?P<address>0x[0-9a-f]+):\s*)'
                            r'(?P<data>(?:\s*0x[0-9a-f]+)+\s*)'),
                           re.IGNORECASE)

    def __init__(self):
        self._registers = OrderedDict()
        self._stack = None
        self._instructions = []

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
