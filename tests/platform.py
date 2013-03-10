# (void)walker unit tests
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

from unittest import TestCase

from framework.interface import Configuration
from framework.platform import CpuFactory
from framework.platform import CpuRepository
from framework.target import InferiorRepository

from application.cpus import MipsCpu
from application.cpus import X8664Cpu
from application.cpus import X86Cpu

from backends.test import TestCpu
from backends.test import TestCpuFactory
from backends.test import TestInferiorFactory
from backends.test import TestThreadFactory
from backends.test import TestPlatformFactory


class CpuTest(TestCase):
    def setUp(self):
        self._cpu_factory = TestCpuFactory()

    def test_test(self):
        cpu_repository = CpuRepository(TestCpuFactory())
        cpu = cpu_repository.get_cpu(TestCpu.architecture())
        for register_list in TestCpu.register_dict.itervalues():
            for name in register_list:
                self.assertIsNotNone(cpu.register(name))
                register = cpu.register(name)
                self.assertEqual(name, register.name())

    def test_x86(self):
        cpu = X86Cpu(self._cpu_factory)
        self.assertIsNotNone(cpu.register('eax'))

    def test_x86_64(self):
        cpu = X8664Cpu(self._cpu_factory)
        self.assertIsNotNone(cpu.register('rax'))

    def test_mips(self):
        cpu = MipsCpu(self._cpu_factory)
        self.assertIsNotNone(cpu.register('a0'))


class ContextTest(TestCase):
    def setUp(self):
        cpu_factory = TestCpuFactory()
        cpu = cpu_factory.create_cpu(TestCpu.architecture())
        inferior_factory = TestInferiorFactory()
        inferior = inferior_factory.create_inferior(cpu, 0)
        self._inferior_repository = InferiorRepository()
        self._inferior_repository.add_inferior(inferior)
        thread_factory = TestThreadFactory()
        thread_factory.create_thread(inferior, 0)
        self._platform_factory = TestPlatformFactory()

    def test_registers(self):
        inferior = self._inferior_repository.get_inferior(0)
        thread = inferior.thread(0)
        context = self._platform_factory.create_context(Configuration(),
                                                        inferior, thread)
        for _, register_dict in inferior.cpu().registers():
            for name, register in register_dict.iteritems():
                self.assertIsNotNone(context.register(name))
                context_register = context.register(name)
                self.assertEqual(register.size(), context_register.size())
                self.assertEqual(register.value(), context_register.value())
