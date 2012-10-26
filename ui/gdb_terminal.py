# (void)walker user interface
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

from ui.terminal import Terminal


class GdbTerminal(Terminal):
    def __init__(self, theme):
        width = gdb.parameter('width')
        height = gdb.parameter('height')
        depth = 256
        super(GdbTerminal, self).__init__(theme, width, height, depth)

    def write(self, string, dictionary=None):
        gdb.write(self.theme().write(string, dictionary))
