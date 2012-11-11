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

from collections import deque


class Thread(object):
    def __init__(self, inferior_id):
        self._inferior_id = inferior_id
        self._contexts = deque()

    def name(self):
        raise NotImplementedError

    def id(self):
        raise NotImplementedError

    def is_valid(self):
        raise NotImplementedError

    def inferior_id(self):
        return self._inferior_id

    def contexts(self):
        return self._contexts
