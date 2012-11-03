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

from collections import OrderedDict

from .factory import PlatformFactory


class Architecture:
    Test = 0
    X86 = 1
    X86_64 = 2
    MIPS = 3
    ARM = 4


class Register(object):
    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def size(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


class Cpu(object):
    def __init__(self, register_list):
        self._registers = OrderedDict()
        for name in iter(register_list):
            self._registers[name] = PlatformFactory().create_register(name)

    @staticmethod
    def architecture():
        raise NotImplementedError

    def register(self, name):
        assert name in self._registers
        return self._registers[name]

    def registers(self):
        return self._registers.iteritems()

    def stack_pointer(self):
        raise NotImplementedError
