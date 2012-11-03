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

from voidwalker.target.inferior import Inferior
from voidwalker.target.inferior import InferiorFactory
from voidwalker.utils.decorators import singleton_implementation

from .platform import TestCpu


class TestInferior(Inferior):
    def __init__(self, cpu):
        super(TestInferior, self).__init__(cpu)


@singleton_implementation(InferiorFactory)
class TestInferiorFactory(object):
    def __init__(self):
        pass

    def create_inferior(self, num):
        cpu = TestCpu()
        return TestInferior(cpu)


class InferiorTest(TestCase):
    def test_inferior(self):
        cpu = TestCpu()
        inferior = InferiorFactory().create_inferior(0)
        self.assertEqual(inferior.cpu().architecture(), cpu.architecture())
