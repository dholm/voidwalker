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

import string

class Widget(object):
    def draw(self, terminal, width):
        raise NotImplementedError()


class Section(Widget):
    _name = None
    _components = None

    def __init__(self, name):
        self._name = name
        self._components = []

    def _draw_header(self, terminal, width):
        header = ''
        if self._name:
            header = '[%s]' % self._name
        dashes = width - len(header)
        terminal.write(('%(face-header)s' + ('-' * dashes) + header) + '\n')

    def add_component(self, component):
        self._components.append(component)

    def draw(self, terminal, width):
        width = (terminal.width() / 5) * 4
        self._draw_header(terminal, width)

        for component in self._components:
            component.draw(terminal, width)


class Table(Widget):
    _cells = None

    class Cell(Widget):
        _contents = None

        def __init__(self, contents):
            assert contents
            self._contents = (' %s ' % contents)

        def width(self, terminal):
            return terminal.string_width(self._contents)

        def draw(self, terminal, width):
            assert self.width(terminal) <= width
            terminal.write(('%(contents)s%(padding)s' %
                            {'contents': self._contents,
                             'padding': ' ' * (width - self.width(terminal))}))

    def _max_cell_width(self, terminal):
        max_width = 0
        for cell in self._cells:
            max_width = max(max_width, cell.width(terminal))
        return max_width

    def __init__(self):
        self._cells = []

    def add_cell(self, cell):
        self._cells.append(cell)

    def draw(self, terminal, width):
        cell_width = self._max_cell_width(terminal)
        cells_per_row = width / cell_width
        assert cells_per_row

        row_padding = (width - (cell_width * cells_per_row))
        terminal.write('%s' % (' ' * row_padding))
        cell_offset = 0
        for cell in self._cells:
            if cells_per_row <= cell_offset:
                cell_offset = 0
                terminal.write('\n%s' % (' ' * row_padding))

            cell.draw(terminal, cell_width)
            cell_offset += 1

        end_padding = (width - (cell_width * cell_offset) - row_padding)
        terminal.write('%s\n' % (' ' * end_padding))
