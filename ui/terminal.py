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

class Terminal(object):
    DEFAULT_WIDTH = 80
    DEFAULT_HEIGHT = 25

    _width = DEFAULT_WIDTH
    _height = DEFAULT_HEIGHT
    _theme = None

    def __init__(self, width, height, theme):
        if width:
            self._width = width
        if height:
            self._height = height
        self._theme = theme

    def string_width(self, string, dictionary=None):
        return self._theme.len(string, dictionary)

    def reset(self):
        self.write(self._theme.reset())

    def width(self):
        return self._width

    def height(self):
        return self._height

    def theme(self):
        return self._theme


class GdbTerminal(Terminal):

    def __init__(self, theme):
        width = gdb.parameter('width')
        height = gdb.parameter('height')
        super(GdbTerminal, self).__init__(width, height, theme)

    def write(self, string, dictionary=None):
        gdb.write(self.theme().write(string, dictionary))
