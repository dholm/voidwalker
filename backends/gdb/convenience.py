# (void)walker GDB backend
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

import gdb

from framework.utils.decorators import singleton


@singleton
class ConvenienceManager(object):
    def __init__(self):
        self._functions = {}

    def init(self):
        pass

    def add_function(self, cls):
        self._functions[cls] = cls()


def register_convenience_function(cls):
    ConvenienceManager().add_function(cls)
