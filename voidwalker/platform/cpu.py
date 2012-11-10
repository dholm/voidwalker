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
    _register_fmt = {16: '0x%032lX',
                     10: '0x%020lX',
                     8: '0x%016lX',
                     4: '0x%08lX',
                     2: '0x%04lX',
                     1: '0x%02lX'}

    def __init__(self, name):
        self._name = name

    def name(self):
        return self._name

    def size(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def str(self):
        if self.value() is not None:
            return self._register_fmt[self.size()] % self.value()
        chars_per_byte = 2
        return ''.join(['-' * (self.size() * chars_per_byte)])


def create_static_register(register):
    class StaticRegister(type(register), object):
        def __init__(self, name):
            super(StaticRegister, self).__init__(name)
            self._size = register.size()
            self._value = register.value()

        def size(self):
            return self._size

        def value(self):
            return self._value

    return StaticRegister(register.name())


class Cpu(object):
    def __init__(self, registers):
        self._registers = OrderedDict()
        for group, register_list in registers.iteritems():
            registers = OrderedDict([(x.name(),
                                      PlatformFactory().create_register(x))
                                     for x in register_list])

            self._registers[group] = registers

    @staticmethod
    def architecture():
        raise NotImplementedError

    def register(self, name):
        for register_dict in self._registers.itervalues():
            if name in register_dict:
                return register_dict[name]

        return None

    def registers(self):
        return self._registers.iteritems()

    def stack_pointer(self):
        raise NotImplementedError

    def program_counter(self):
        raise NotImplementedError
