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

from framework.target.inferior import InferiorManager
from framework.target.inferior import TargetFactory

from .platform import TestCpu


class InferiorTest(TestCase):
    def setUp(self):
        TargetFactory().create_inferior(0)
        inferior = InferiorManager().inferior(0)
        TargetFactory().create_thread(inferior, 0)

    def test_inferior(self):
        inferior = InferiorManager().inferior(0)
        self.assertEqual(0, inferior.id())
        self.assertEqual(inferior.cpu().architecture(),
                         TestCpu().architecture())

    def test_thread(self):
        inferior = InferiorManager().inferior(0)
        self.assertTrue(inferior.has_thread(0))
        thread = inferior.thread(0)
        self.assertEqual(0, thread.id())
