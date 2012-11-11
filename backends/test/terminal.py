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

import os
from sys import stdout

from framework.ui.terminal import Terminal
from framework.ui.theme import ThemeManager

from application.parameters.ui import ThemeParameter


class SysTerminal(Terminal, object):
    def _theme(self):
        return ThemeManager().theme(ThemeParameter.get_value())

    def __init__(self):
        width = int(os.popen('tput cols').read().strip())
        height = int(os.popen('tput lines').read().strip())
        depth = int(os.popen('tput colors').read().strip())
        super(SysTerminal, self).__init__(width, height, depth)

    def theme(self):
        return self._theme()

    def write(self, string, dictionary=None):
        stdout.write(self._theme().write(string, dictionary))
