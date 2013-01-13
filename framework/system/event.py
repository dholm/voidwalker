# (void)walker event processing
# Copyright (C) 2013 David Holm <dholmster@gmail.com>

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

from collections import deque


class Event(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    def eval(self, *args, **kwargs):
        raise NotImplementedError()

    def __call__(self):
        self.eval(*self._args, **self._kwargs)


class EventQueue(object):
    def __init__(self):
        self._queue = deque()

    def __nonzero__(self):
        return bool(self._queue)

    def onEnqueue(self):
        raise NotImplementedError()

    def enqueue(self, event):
        self._queue.append(event)
        self.onEnqueue()

    def dequeue(self):
        return self._queue.pop()
