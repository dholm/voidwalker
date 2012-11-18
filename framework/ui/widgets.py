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

import re
import textwrap


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
        title = ''
        if self._name:
            title = ('[%s]' % self._name)
        assert terminal.string_width(title) <= width

        header = ['%(face-header)s']
        dashes = width - len(title)
        header += ['-' for i in range(dashes)]
        header += [title, '\n']
        terminal.write(''.join(header))

    def add_component(self, component):
        self._components.append(component)

    def draw(self, terminal, width):
        width -= (width / 20)
        self._draw_header(terminal, width)

        for component in self._components:
            component.draw(terminal, width)


class Table(Widget):
    class Cell(Widget):
        _format_exp = re.compile(r'(%\([^\s]+?\)s)')

        def __init__(self, contents=''):
            super(Table.Cell, self).__init__()
            self._contents = ''
            if contents:
                self._contents = (' %s ' % contents)

        def width(self, terminal):
            return terminal.string_width(self._contents)

        def contents(self):
            return self._contents

        def draw(self, terminal, width):
            split = self._format_exp.split(self._contents)
            contents = [[]]
            width_left = width
            last_format = ''
            for item in split:
                if self._format_exp.match(item):
                    contents[-1].append(item)
                    last_format = item

                else:
                    item_len = len(item.replace('%%', '%'))
                    if item_len <= width_left:
                        contents[-1].append(item)
                        width_left -= item_len

                    elif item_len < width:
                        contents.append([last_format, item])
                        width_left = width - item_len

                    elif len(item[:width_left]):
                        first = textwrap.wrap(item[:width_left], width_left)[0]
                        contents[-1].append(first)
                        rest = textwrap.wrap(item[len(first):], width)
                        for line in rest:
                            contents.append([last_format, line])
                        width_left = width - len(contents[-1][-1])

            contents = [''.join(x) for x in contents]
            cell_content = ''
            if len(contents):
                cell_content = contents[0]

            line_width = terminal.string_width(cell_content)
            padding = ' ' * (width - line_width)
            terminal.write(('%(contents)s%(padding)s' %
                            {'contents': cell_content,
                             'padding': padding}))

            return ''.join(contents[1:])

    class Row(Widget):
        def __init__(self):
            super(Table.Row, self).__init__()
            self._cells = []

        def cells(self):
            return self._cells

        def add_cell(self, cell):
            self._cells.append(cell)

        def width(self, terminal):
            width = 0
            for cell in self._cells:
                width += cell.width(terminal)
            return width

        def draw(self, terminal, cell_widths):
            assert len(cell_widths) == len(self._cells)

            cells_rest = []
            for i in range(len(self._cells)):
                rest = self._cells[i].draw(terminal, cell_widths[i])
                if len(rest):
                    cells_rest.append(rest)
                else:
                    cells_rest.append(None)

            if cells_rest.count(None) < len(cells_rest):
                row = Table.Row()
                for content in cells_rest:
                    if content is None:
                        row.add_cell(Table.Cell(''))
                    else:
                        row.add_cell(Table.Cell(content))
                return row
            return None

    def _max_cell_width(self, terminal):
        max_width = 0
        for cell in self._cells:
            max_width = max(max_width, cell.width(terminal))
        return max_width

    def __init__(self):
        self._rows = []
        self._cols_per_row = 0
        self._cells = []

    def add_cell(self, cell):
        assert isinstance(cell, Table.Cell)
        self._cells.append(cell)

    def add_row(self, row):
        assert isinstance(row, Table.Row)
        self._cols_per_row = max(len(row.cells()), self._cols_per_row)
        self._rows.append(row)

    def _draw_cells(self, terminal, width):
        cell_width = self._max_cell_width(terminal)
        cells_per_row = width / cell_width
        assert cells_per_row

        cell_row_width = (cell_width * cells_per_row)
        row_padding_begin = (width - cell_row_width) / 2
        row_padding_end = (width - cell_row_width - row_padding_begin)

        terminal.write('%s' % (' ' * row_padding_begin))
        cell_offset = 0
        for cell in self._cells:
            if cells_per_row <= cell_offset:
                cell_offset = 0
                terminal.write(('%s\n%s' % (' ' * row_padding_end,
                                            ' ' * row_padding_begin)))

            cell.draw(terminal, cell_width)
            cell_offset += 1

        last_row_padding = (width - (cell_width * cell_offset) -
                            row_padding_begin)
        terminal.write('%s\n' % (' ' * last_row_padding))

    def _cols_median(self, terminal):
        cols_width = [[0 for i in range(len(self._rows))]
                      for j in range(self._cols_per_row)]
        for i in range(len(self._rows)):
            row = self._rows[i]
            for j in range(len(row.cells())):
                cell = row.cells()[j]
                cols_width[j][i] = cell.width(terminal)

        cols_median = [0 for i in range(len(cols_width))]
        for i in range(len(cols_width)):
            lst = sorted(cols_width[i])
            length = len(lst)
            if not length % 2:
                cols_median[i] = int((lst[length / 2] + lst[length / 2 - 1]) /
                                     2)
            else:
                cols_median[i] = lst[length / 2]

        return cols_median

    def _cols_mean(self, terminal):
        cols_width = [[0 for i in range(len(self._rows))]
                      for j in range(self._cols_per_row)]
        for i in range(len(self._rows)):
            row = self._rows[i]
            for j in range(len(row.cells())):
                cell = row.cells()[j]
                cols_width[j][i] = cell.width(terminal)

        cols_mean = [0 for i in range(len(cols_width))]
        for i in range(len(cols_width)):
            cols_mean[i] = int(sum(cols_width[i]) / len(cols_width[i]))

        return cols_mean

    def _fill_widths(self, widths, wanted_widths, max_widths):
        for i in range(len(max_widths)):
            if widths[i] is not None:
                continue
            elif wanted_widths[i] <= max_widths[i]:
                widths[i] = wanted_widths[i]

        return widths

    def _col_widths(self, terminal, width):
        cell_widths = []
        for row in self._rows:
            cells = len(row.cells())
            cell_widths.extend([0] * (cells - len(cell_widths)))

            for i in range(len(row.cells())):
                cell_widths[i] = max(cell_widths[i],
                                     row.cells()[i].width(terminal))

        if width < sum(cell_widths):
            adjusted_widths = [None] * len(cell_widths)

            mean_widths = [(int(width / len(cell_widths)))] * len(cell_widths)
            adjusted_widths = self._fill_widths(adjusted_widths, cell_widths,
                                                mean_widths)
            mean_widths = self._cols_mean(terminal)
            median_widths = self._cols_median(terminal)
            if adjusted_widths.count(None):
                left_width = width - sum(filter(None, adjusted_widths))
                max_cell_width = int(left_width / adjusted_widths.count(None))
                max_widths = [min(max(mean_widths[i], median_widths[i]),
                                  max_cell_width)
                              for i in range(len(cell_widths))]
                adjusted_widths = self._fill_widths(adjusted_widths,
                                                    cell_widths, max_widths)

            while adjusted_widths.count(None):
                left_width = width - sum(filter(None, adjusted_widths))
                max_cell_width = int(left_width / adjusted_widths.count(None))
                current_min = min([cell_widths[i]
                                   for i in range(len(cell_widths))
                                   if adjusted_widths[i] is None])
                index = cell_widths.index(current_min)
                adjusted_widths[index] = max_cell_width

            return adjusted_widths

        return cell_widths

    def _draw_rows(self, terminal, width):
        cell_widths = self._col_widths(terminal, width)
        row_width = sum(cell_widths)
        for row in self._rows:
            while row is not None:
                row = row.draw(terminal, cell_widths)
                padding = ' ' * (width - row_width)
                terminal.write('%s\n' % padding)

    def draw(self, terminal, width):
        if self._rows:
            self._draw_rows(terminal, width)
        if self._cells:
            self._draw_cells(terminal, width)
