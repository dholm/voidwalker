# (void)walker target support
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

from collections import deque


class Thread(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, inferior):
        self._inferior = inferior
        self._contexts = deque()

    def get_inferior(self):
        return self._inferior

    def contexts(self):
        return self._contexts

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError

    @abc.abstractmethod
    def id(self):
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid(self):
        raise NotImplementedError


class ThreadFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_thread(self, inferior, thread_id):
        raise NotImplementedError
