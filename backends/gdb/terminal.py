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
import tempfile

from flowui import Terminal


class GdbTerminal(Terminal):
    def _get_depth(self):
        tf = tempfile.NamedTemporaryFile(delete=True)
        gdb.execute('shell tput colors >%s' % tf.name, False, True)
        tf.flush()
        try:
            return int(tf.read().strip())
        except ValueError:
            return Terminal.DEFAULT_DEPTH

    def reset(self):
        pass

    def __init__(self):
        width = gdb.parameter('width')
        height = gdb.parameter('height')
        depth = self._get_depth()
        super(GdbTerminal, self).__init__(width, height, depth)

    def write(self, string, dictionary=None):
        if dictionary is not None:
            string = string.format(dictionary)
        gdb.write(string)
