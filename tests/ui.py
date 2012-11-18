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

from unittest import TestCase

from framework.ui.theme import ThemeManager
from framework.ui.widgets import Section
from framework.ui.widgets import Table

from application.themes.solarized import Solarized
from application.themes.zenburn import Zenburn

from backends.test.terminal import SysTerminal


class ThemeTest(object):
    def setUp(self):
        self._terminal = SysTerminal()
        ThemeManager().init(self._terminal.depth())

    def tearDown(self):
        reset = self.theme().property('normal')
        self.terminal().write('%s\n' % reset)

    def theme(self):
        raise NotImplementedError()

    def terminal(self):
        return self._terminal

    def test_faces(self):
        reset = self.theme().property('normal')
        self.terminal().write('\n')
        for name, face in self.theme().faces().iteritems():
            self.terminal().write(self.theme().write('\t%s[%s]%s\n' %
                                                     (face, name, reset)))


class SolarizedTest(ThemeTest, TestCase):
    def theme(self):
        return ThemeManager().theme(Solarized.name())


class ZenburnTest(ThemeTest, TestCase):
    def theme(self):
        return ThemeManager().theme(Zenburn.name())


class WidgetsTest(TestCase):
    def theme(self):
        return self._terminal.theme()

    def setUp(self):
        self._theme = ThemeManager().theme(Solarized.name())
        self._terminal = SysTerminal()

        reset = self.theme().property('normal')
        self._terminal.write('%s\n\t# Begin Widget #\n' % reset)

    def tearDown(self):
        reset = self.theme().property('normal')
        self._terminal.write('%s\t# End Widget #\n' % reset)

    def test_section(self):
        section = Section('test section')
        section.draw(self._terminal, self._terminal.width())

        self.assertRaises(AssertionError, section.draw, self._terminal, 1)

    def test_table(self):
        table = Table()
        table.draw(self._terminal, self._terminal.width())

    def test_tables_cells(self):
        table = Table()
        for i in range(0, 20):
            cell = Table.Cell('cell %d' % i)
            table.add_cell(cell)

        table.draw(self._terminal, self._terminal.width() / 2)

    def test_table_row_multiline_cell(self):
        row = Table.Row()
        cells = [Table.Cell('First col'),
                 Table.Cell('this cell should span multiple lines'),
                 Table.Cell('Third col')]
        for cell in cells:
            row.add_cell(cell)
        row_len = (sum(x.width(self._terminal) for x in cells) -
                   (cells[1].width(self._terminal) / 2))

        table = Table()
        table.add_row(row)
        table.draw(self._terminal, row_len)

    def test_tables_rows(self):
        table = Table()
        for i in range(0, 5):
            row = Table.Row()
            for j in range(0, 5):
                cell = Table.Cell('cell %d,%d' % (i, j))
                row.add_cell(cell)

            table.add_row(row)

        table.draw(self._terminal, self._terminal.width() / 2)

    def test_table_cells_rows(self):
        table = Table()
        for i in range(0, 5):
            row = Table.Row()
            for j in range(0, 5):
                cell = Table.Cell('cell %d,%d' % (i, j))
                row.add_cell(cell)

            table.add_row(row)
            cell = Table.Cell('cell %d' % i)
            table.add_cell(cell)

        table.draw(self._terminal, self._terminal.width() / 2)

    def test_table_rows_varying_cells(self):
        data = [['col 1', 'col 2', 'col 3'],
                ['xxYYxxYYxx', '-', ''],
                ['', '-', 'xxYYxxYY']]

        table = Table()
        for r in data:
            row = Table.Row()
            for c in r:
                row.add_cell(Table.Cell(c))

            table.add_row(row)

        table.draw(self._terminal, self._terminal.width())
