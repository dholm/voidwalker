# (void)walker basic types
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

import string

from flowui import Widget
from flowui.widgets.table import Cell
from flowui.widgets.table import Row
from flowui.widgets.table import Table

from ..utils.recipes import grouper


class DataChunk(object):
    def __init__(self, address, data_buffer):
        self._address = address
        self._buffer = data_buffer

    def __len__(self):
        return len(self._buffer)

    def address(self):
        return self._address

    def buffer(self):
        return self._buffer


class DataWidget(Widget):
    _ascii_filter = ''.join([['.', chr(x)]
                             [chr(x) in string.printable[:-5]]
                             for x in xrange(256)])

    def __init__(self, data_chunk):
        super(DataWidget, self).__init__()
        self._data_chunk = data_chunk

    def draw(self, terminal, width):
        table = Table()

        line_len = 16
        if width < 100:
            line_len = 8

        address = self._data_chunk.address()
        for line in grouper(line_len, self._data_chunk.buffer()):
            hex_string = []
            ascii_string = []
            for octuple in grouper(8, line):
                for quadruple in grouper(4, octuple):
                    hex_string += [(' %02X' % ord(i))
                                   for i in quadruple
                                   if i is not None]
                    filtered = ''.join([x.translate(self._ascii_filter)
                                        for x in quadruple
                                        if x is not None])
                    ascii_string += filtered.replace('%', '%%')

                hex_string += ['  ']
                ascii_string += ['  ']

            row = Row()
            row.add_cell(Cell('0x%016X:' % address))
            row.add_cell(Cell(''.join(hex_string)))
            row.add_cell(Cell(''.join(ascii_string)))
            table.add_row(row)

            address += line_len

        table.draw(terminal, width)
