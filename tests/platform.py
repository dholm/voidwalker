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

from framework.platform.architecture import ArchitectureManager
from framework.platform.factory import PlatformFactory
from framework.target.inferior import InferiorManager
from framework.target.inferior import TargetFactory

from application.cpus.mips import MipsCpu
from application.cpus.x86 import X86Cpu
from application.cpus.x86_64 import X8664Cpu

from backends.test.platform import TestCpu


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
