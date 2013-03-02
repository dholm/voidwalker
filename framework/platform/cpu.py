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

import abc

from collections import OrderedDict

from ..utils import enum
from .factory import PlatformFactory


Architecture = enum('Test', 'X86', 'X8664', 'Mips', 'Arm',
                    enum_type='Architecture')


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
    __metaclass__ = abc.ABCMeta

    def __init__(self, registers):
        self._registers = OrderedDict()
        for group, register_list in registers.iteritems():
            registers = OrderedDict([(x.name(),
                                      PlatformFactory().create_register(x))
                                     for x in register_list])

            self._registers[group] = registers

    @staticmethod
    @abc.abstractmethod
    def architecture():
        raise NotImplementedError

    def register(self, name):
        for register_dict in self._registers.itervalues():
            if name in register_dict:
                return register_dict[name]

        return None

    def registers(self):
        return self._registers.iteritems()

    @abc.abstractmethod
    def stack_pointer(self):
        raise NotImplementedError

    @abc.abstractmethod
    def program_counter(self):
        raise NotImplementedError


class CpuFactory(object):
    def create(self, architecture):
        assert architecture in _architecture_map
        return _architecture_map.get(architecture, None)()


def register_cpu(cls):
    _architecture_map[cls.architecture()] = cls
    return cls

_architecture_map = {}
