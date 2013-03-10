# (void)walker target support
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


class Inferior(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, cpu):
        self._cpu = cpu
        self._threads = {}

    @abc.abstractmethod
    def id(self):
        raise NotImplementedError

    def cpu(self):
        return self._cpu

    def has_thread(self, thread_id):
        return thread_id in self._threads

    def add_thread(self, thread):
        self._threads[thread.id()] = thread

    def thread(self, thread_id):
        assert self.has_thread(thread_id)
        return self._threads[thread_id]

    @abc.abstractmethod
    def disassemble(self, address, length):
        raise NotImplementedError

    @abc.abstractmethod
    def read_memory(self, address, length):
        raise NotImplementedError

    @abc.abstractmethod
    def write_memory(self, buf, address):
        raise NotImplementedError


class InferiorFactory(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, cpu_factory):
        self._cpu_factory = cpu_factory

    @abc.abstractmethod
    def create_inferior(self, inferior_id):
        raise NotImplementedError


class InferiorRepository(object):
    def __init__(self):
        self._inferiors = {}

    def add_inferior(self, inferior):
        self._inferiors[inferior.id()] = inferior

    def has_inferior(self, inferior_id):
        return inferior_id in self._inferiors

    def get_inferior(self, inferior_id):
        assert self.has_inferior(inferior_id), ('inferior %r not found' %
                                                inferior_id)
        return self._inferiors[inferior_id]
