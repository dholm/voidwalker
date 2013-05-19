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

from voidwalker.framework.platform import CpuFactory
from voidwalker.framework.target import InferiorRepository

from voidwalker.backends.test import TestPlatformFactory
from voidwalker.backends.test import TestThreadFactory
from voidwalker.backends.test import TestInferiorFactory

from voidwalker.backends.test.platform import TestCpuFactory
from voidwalker.backends.test.target import TestInferiorFactory
from voidwalker.backends.test.target import TestThreadFactory


class InferiorTest(TestCase):
    def setUp(self):
        cpu_factory = TestCpuFactory()
        self._cpu = cpu_factory.create_cpu(None)

    def test_inferior_repository(self):
        inferior_repository = InferiorRepository()
        self.assertFalse(inferior_repository.has_inferior(0))

    def test_inferior(self):
        inferior_factory = TestInferiorFactory()
        inferior = inferior_factory.create_inferior(self._cpu, 0)

        self.assertEqual(0, inferior.id())
        self.assertEqual(inferior.cpu().architecture(),
                         self._cpu.architecture())

    def test_thread(self):
        inferior_factory = TestInferiorFactory()
        inferior = inferior_factory.create_inferior(self._cpu, 0)
        thread_factory = TestThreadFactory()
        thread = thread_factory.create_thread(inferior, 0)
        inferior.add_thread(thread)

        self.assertTrue(inferior.has_thread(0))
        thread = inferior.thread(0)
        self.assertEqual(0, thread.id())
