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

from collections import OrderedDict
from unittest import TestCase

from voidwalker.platform.architecture import ArchitectureManager
from voidwalker.platform.architecture import register_cpu
from voidwalker.platform.context import Context
from voidwalker.platform.cpu import Architecture
from voidwalker.platform.cpu import Cpu
from voidwalker.platform.cpu import Register
from voidwalker.platform.cpu import create_static_register
from voidwalker.platform.cpus.mips import MipsCpu
from voidwalker.platform.cpus.x86 import X86Cpu
from voidwalker.platform.cpus.x86_64 import X8664Cpu
from voidwalker.platform.factory import PlatformFactory
from voidwalker.target.inferior import InferiorManager
from voidwalker.target.inferior import TargetFactory
from voidwalker.utils.decorators import singleton_implementation


@register_cpu
class TestCpu(Cpu):
    register_dict = OrderedDict([('gp', ('r0 r1').split()),
                                 ('sp', ('pc sp flags').split())])

    def __init__(self):
        registers = OrderedDict()
        for group, register_list in self.register_dict.iteritems():
            registers[group] = [Register(x) for x in register_list]
        super(TestCpu, self).__init__(registers)

    @staticmethod
    def architecture():
        return Architecture.Test

    def stack_pointer(self):
        return self.register('sp')

    def instruction_pointer(self):
        return self.register('pc')


@singleton_implementation(PlatformFactory)
class PlatformFactoryTest(object):
    def __init__(self):
        self._registers = None
        self.reset()

    def reset(self):
        self._registers = {}

    def create_register(self, register):
        class TestRegister(type(register), object):
            def __init__(self, name):
                super(TestRegister, self).__init__(name)
                self._size = 8
                self._value = 0

            def size(self):
                return self._size

            def value(self):
                return self._value

        self._registers[register.name()] = TestRegister(register.name())
        return self._registers[register.name()]

    def create_context(self, inferior, thread):
        class TestContext(Context):
            def __init__(self):
                sp = inferior.cpu().stack_pointer()
                super(TestContext, self).__init__(sp)

                for group, register_dict in inferior.cpu().registers():
                    register_dict = dict((x.name(), create_static_register(x))
                                         for x in register_dict.itervalues())
                    self._registers[group] = register_dict

        return TestContext()


class CpuTest(TestCase):
    def setUp(self):
        PlatformFactory().reset()

    def test_test(self):
        cpu = ArchitectureManager().create_cpu(TestCpu.architecture())
        for register_list in TestCpu.register_dict.itervalues():
            for name in register_list:
                self.assertIsNotNone(cpu.register(name))
                register = cpu.register(name)
                self.assertEqual(name, register.name())

    def test_x86(self):
        cpu = ArchitectureManager().create_cpu(X86Cpu.architecture())
        self.assertIsNotNone(cpu.register('eax'))

    def test_x86_64(self):
        cpu = ArchitectureManager().create_cpu(X8664Cpu.architecture())
        self.assertIsNotNone(cpu.register('rax'))

    def test_mips(self):
        cpu = ArchitectureManager().create_cpu(MipsCpu.architecture())
        self.assertIsNotNone(cpu.register('a0'))


class ContextTest(TestCase):
    def setUp(self):
        TargetFactory().create_inferior(0)
        inferior = InferiorManager().inferior(0)
        TargetFactory().create_thread(inferior, 0)

    def test_registers(self):
        inferior = InferiorManager().inferior(0)
        thread = inferior.thread(0)
        context = PlatformFactory().create_context(inferior, thread)
        for group, register_dict in inferior.cpu().registers():
            for name, register in register_dict.iteritems():
                self.assertIsNotNone(context.register(name))
                context_register = context.register(name)
                self.assertEqual(register.size(), context_register.size())
                self.assertEqual(register.value(), context_register.value())
