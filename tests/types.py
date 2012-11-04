# (void)walker unit tests
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

from array import array
from unittest import TestCase

from voidwalker.ui.terminal import SysTerminal
from voidwalker.types.data import DataChunk
from voidwalker.types.data import DataWidget


class WidgetsTest(TestCase):
    def setUp(self):
        self._terminal = SysTerminal()

    def test_datachunk(self):
        address = 0xf00fba11
        data = array('c', ['\x00', '\x01', '\xff', '\x12'])
        data_chunk = DataChunk(address, buffer(data))
        self.assertEqual(address, data_chunk.address())
        self.assertItemsEqual(data, data_chunk.buffer())

    def test_datawidget(self):
        address = 0xf00fba11
        data = '\x00test\x12\x67\x90\xff\x0042\xff\x15\x16'
        data_chunk = DataChunk(address, buffer(data))
        data_widget = DataWidget(data_chunk)

        self._terminal.write('\n\t# Current terminal width #\n')
        data_widget.draw(self._terminal, self._terminal.width())

        self._terminal.write(('\n\t# Default width (%d) #\n' %
                              self._terminal.DEFAULT_WIDTH))
        data_widget.draw(self._terminal, self._terminal.DEFAULT_WIDTH)
