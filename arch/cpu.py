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
from collections import OrderedDict


class Register(object):
    _name = None

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def size(self):
        size = gdb.parse_and_eval('sizeof($' + self._name + ')')
        try:
            return int(size)
        except gdb.error:
            return None

    def value(self):
        value = gdb.parse_and_eval('$' + self._name)
        try:
            return long(value)
        except gdb.error:
            return None


class Cpu(object):
    _registers = None

    def __init__(self, register_list):
        self._registers = OrderedDict()
        for name in iter(register_list):
            self._registers[name] = Register(name)

    def register(self, name):
        assert name in self._registers
        return self._registers[name]

    def registers(self):
        return self._registers.iteritems()

    def stack_pointer(self):
        return None
