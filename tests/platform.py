# (void)walker unit tests
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

from unittest import TestCase

from voidwalker.platform.architecture import ArchitectureManager
from voidwalker.platform.architecture import register_cpu
from voidwalker.platform.context import Context
from voidwalker.platform.context import ContextRegister
from voidwalker.platform.cpu import Architecture
from voidwalker.platform.cpu import Cpu
from voidwalker.platform.cpu import Register
from voidwalker.platform.cpus.mips import MipsCpu
from voidwalker.platform.cpus.x86_64 import X8664Cpu
from voidwalker.platform.factory import PlatformFactory
from voidwalker.utils.decorators import singleton_implementation


@register_cpu
class TestCpu(Cpu):
    register_list = ('r0 r1 sp').split()

    def __init__(self):
        super(TestCpu, self).__init__(self.register_list)

    @staticmethod
    def architecture():
        return Architecture.Test

    def stack_pointer(self):
        return self.register('sp')


@singleton_implementation(PlatformFactory)
class PlatformFactoryTest(object):
    def __init__(self):
        self._registers = None
        self.reset()

    def reset(self):
        self._registers = {}

    def create_register(self, name):
        class TestRegister(Register):
            def __init__(self, name):
                super(TestRegister, self).__init__(name)
                self._size = 8
                self._value = 0

            def size(self):
                return self._size

            def value(self):
                return self._value

        self._registers[name] = TestRegister(name)
        return self._registers[name]

    def create_context(self, cpu):
        class TestContext(Context):
            def __init__(self, cpu):
                super(TestContext, self).__init__(cpu)

                for name, register in self.cpu().registers():
                    self._registers[name] = ContextRegister(register)

        return TestContext(cpu)


class CpuTest(TestCase):
    def setUp(self):
        PlatformFactory().reset()

    def test_test(self):
        cpu = ArchitectureManager().create_cpu(TestCpu.architecture())
        for name in TestCpu.register_list:
            self.assertIsNotNone(cpu.register(name))
            register = cpu.register(name)
            self.assertEqual(name, register.name())

    def test_x86_64(self):
        cpu = ArchitectureManager().create_cpu(X8664Cpu.architecture())
        self.assertIsNotNone(cpu.register('rax'))

    def test_mips(self):
        cpu = ArchitectureManager().create_cpu(MipsCpu.architecture())
        self.assertIsNotNone(cpu.register('a0'))


class ContextTest(TestCase):
    def test_registers(self):
        cpu = ArchitectureManager().create_cpu(TestCpu.architecture())
        context = PlatformFactory().create_context(cpu)
        self.assertEqual(cpu, context.cpu())
        for name, register in cpu.registers():
            self.assertIsNotNone(context.register(name))
            context_register = context.register(name)
            self.assertEqual(register.size(), context_register.size())
            self.assertEqual(register.value(), context_register.value())
