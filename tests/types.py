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
from flowui.terminal import AnsiTerminal
from flowui.terminals import SysTerminal
from flowui.themes import Solarized
from unittest import TestCase

from framework.types.data import DataChunk
from framework.types.data import DataWidget
from framework.types.instructions import Instruction
from framework.types.instructions import InstructionListing
from framework.types.instructions import InstructionListingWidget


class WidgetsTest(TestCase):
    def _draw_widget(self, widget):
        self._terminal.write('\n\t# Current terminal width #\n')
        widget.draw(self._terminal, self._terminal.width())

        self._terminal.write(('\n\t# Default width (%d) #\n' %
                              self._terminal.DEFAULT_WIDTH))
        widget.draw(self._terminal, self._terminal.DEFAULT_WIDTH)

    def setUp(self):
        self._terminal = AnsiTerminal(SysTerminal(), Solarized())

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
        self._draw_widget(data_widget)

    def test_instruction(self):
        opcode = array('c', ['\x83', '\xc0', '\x02'])
        mnemonic = 'add'
        operands = '$0x2,%%eax'
        symbol = '<main+20>'
        instruction = Instruction(opcode, mnemonic, operands, symbol)
        self.assertEqual(opcode, instruction.opcode())
        self.assertEqual(mnemonic, instruction.mnemonic())
        self.assertEqual(operands, instruction.operands())
        self.assertEqual(symbol, instruction.symbol())

    def test_instruction_listing(self):
        listing = InstructionListing()
        listing.add_instruction(0xed4, Instruction(array('c', ['\x83', '\xc0',
                                                               '\x02']),
                                                   'add', '$0x2,%%eax',
                                                   '<main+20>'))
        long_symbol_name = ['x' for _ in range(self._terminal.DEFAULT_WIDTH)]
        listing.add_instruction(0xed7, Instruction(array('c', ['\x48', '\x89',
                                                               '\xc7']),
                                                   'mov', '%%rax,%%rdi',
                                                   ''.join(long_symbol_name)))

        listing_widget = InstructionListingWidget(listing, 0xed4)
        self._draw_widget(listing_widget)
