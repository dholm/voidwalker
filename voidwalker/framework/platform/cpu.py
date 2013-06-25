# (void)walker hardware platform support
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

import abc

from ..utils import OrderedDict
from ..utils import enum


Architecture = enum('Test', 'X86', 'X8664', 'Mips', 'Arm', 'Generic',
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

    def __init__(self, cpu_factory, registers):
        self._registers = OrderedDict()
        for group, register_list in registers.iteritems():
            registers = OrderedDict([(x.name(),
                                      cpu_factory.create_register(self, x))
                                     for x in register_list])

            self._registers[group] = registers

    @classmethod
    @abc.abstractmethod
    def architecture(cls):
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
    __metaclass__ = abc.ABCMeta

    def create_cpu(self, architecture):
        assert architecture in _cpu_map
        return _cpu_map.get(architecture,
                            None)(self)

    @abc.abstractmethod
    def create_register(self, cpu, register):
        raise NotImplementedError


class CpuRepository(object):
    def __init__(self, cpu_factory):
        self._cpu_factory = cpu_factory
        self._cpus = {}

    def get_cpu(self, architecture):
        if architecture in self._cpus:
            return self._cpus[architecture]
        cpu = self._cpu_factory.create_cpu(architecture)
        self._cpus[architecture] = cpu
        return cpu


def register_cpu(cls):
    _cpu_map[cls.architecture()] = cls
    return cls

_cpu_map = {}
