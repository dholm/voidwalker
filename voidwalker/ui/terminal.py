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

import os
from sys import stdout

from ..interface.parameter import ParameterManager
from ..interface.parameters.ui import ThemeParameter
from .theme import ThemeManager


class Terminal(object):
    DEFAULT_WIDTH = 80
    DEFAULT_HEIGHT = 25
    DEFAULT_DEPTH = 8

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT,
                 depth=DEFAULT_DEPTH):
        self._width = width
        self._height = height
        self._depth = depth

    def string_width(self, string, dictionary=None):
        return self.theme().len(string, dictionary)

    def write(self, string, dictionary=None):
        raise NotImplementedError()

    def reset(self):
        self.write(self.theme().property('normal'))

    def depth(self):
        return self._depth

    def width(self):
        return self._width

    def height(self):
        return self._height

    def theme(self):
        name = ParameterManager().get_parameter(ThemeParameter.name()).value
        return ThemeManager().theme(name)


class SysTerminal(Terminal):
    def __init__(self):
        width = int(os.popen('tput cols').read().strip())
        height = int(os.popen('tput lines').read().strip())
        depth = int(os.popen('tput colors').read().strip())
        super(SysTerminal, self).__init__(width, height, depth)

    def write(self, string, dictionary=None):
        stdout.write(self.theme().write(string, dictionary))
