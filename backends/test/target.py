# (void)walker unit test backend
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

from framework.target import Inferior
from framework.target import TargetFactory
from framework.target import Thread

from .platform import TestCpu


class TestThread(Thread):
    def __init__(self, inferior_id, thread_id):
        super(TestThread, self).__init__(inferior_id)
        self._thread_id = thread_id

    def name(self):
        return ('thread %d' % self._thread_id)

    def id(self):
        return self._thread_id

    def is_valid(self):
        return True


class TestInferior(Inferior):
    def __init__(self, cpu, inferior_id):
        super(TestInferior, self).__init__(cpu)
        self._id = inferior_id

    def id(self):
        return self._id

    def disassemble(self, address, length):
        return None

    def read_memory(self, address, length):
        return None

    def write_memory(self, buf, address):
        pass


class TestTargetFactory(TargetFactory, object):
    def __init__(self, cpu_factory):
        self._cpu_factory = cpu_factory

    def create_inferior(self, inferior_id):
        cpu = self._cpu_factory.create(TestCpu.architecture())
        return TestInferior(cpu, inferior_id)

    def create_thread(self, inferior, thread_id):
        thread = TestThread(inferior.id(), thread_id)
        inferior.add_thread(thread)
        return thread
