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

import re

from collections import OrderedDict
from flowui import Widget
from flowui.widgets.table import Cell
from flowui.widgets.table import Row
from flowui.widgets.table import Table


class Instruction(object):
    def __init__(self, opcode, mnemonic, operands, symbol=None):
        self._opcode = opcode
        self._mnemonic = mnemonic
        self._operands = operands
        self._symbol = symbol

    def opcode(self):
        return self._opcode

    def mnemonic(self):
        return self._mnemonic

    def operands(self):
        return self._operands

    def symbol(self):
        return self._symbol


class InstructionListing(object):
    def __init__(self):
        self._instructions = OrderedDict()

    def __len__(self):
        return len(self._instructions)

    def instructions(self):
        return self._instructions.iteritems()

    def add_instruction(self, address, instruction):
        self._instructions[address] = instruction


class InstructionListingWidget(Widget):
    _operands_scanner = re.Scanner([
        (r'[\$-]?0[xX]([0-9A-Fa-f]+)',
         lambda scanner, token:('CONSTANT', token)),
        (r'[\$-]?\d+h?', lambda scanner, token:('CONSTANT', token)),
        (r'%*[A-Za-z_][A-Za-z0-9_]*',
         lambda scanner, token:('IDENTIFIER', token)),
        (r'<[^>]+>',
         lambda scanner, token:('SYMBOL', token)),
        (r'[,]+', lambda scanner, token:('PUNCTUATION', token)),
        (r'[-+*:$\(\)]', lambda scanner, token:('OPERAND', token)),
        (r'#.*$', lambda scanner, token:('COMMENT', token)),
        (r'\s+', lambda scanner, token:('WHITESPACE', token))])
    _operands_face = {'CONSTANT': '%(face-constant)s',
                      'IDENTIFIER': '%(face-identifier)s',
                      'SYMBOL': '%(face-type)s',
                      'PUNCTUATION': '',
                      'OPERAND': '',
                      'COMMENT': '%(face-comment)s',
                      'WHITESPACE': ''}

    def __init__(self, instruction_listing, program_counter=None):
        self._instruction_listing = instruction_listing
        self._program_counter = program_counter

    def _fmt_operands(self, operands):
        operands_list = []
        parsed, remainder = self._operands_scanner.scan(operands)
        for token in parsed:
            face = self._operands_face.get(token[0], '')
            operands_list.append(face)
            operands_list.append(token[1])
            if len(face):
                operands_list.append('%(face-normal)s')

        return ''.join(operands_list + [remainder])

    def draw(self, terminal, width):
        table = Table()
        for address, instruction in self._instruction_listing.instructions():
            row = Row()

            const_face = '%(face-normal)s'
            if address == self._program_counter:
                const_face = '%(face-underlined)s'
            row.add_cell(Cell('%s0x%016lX:' % (const_face, address)))

            if instruction.symbol() is not None:
                identifier = ['%(face-identifier)s', instruction.symbol(), ':']
                row.add_cell(Cell(''.join(identifier)))
            else:
                row.add_cell(Cell())

            hex_string = [('%02X' % ord(i))
                          for i in instruction.opcode()
                          if i is not None]
            row.add_cell(Cell('%s%s' % (const_face, ' '.join(hex_string))))

            row.add_cell(Cell('%s%s' % ('%(face-statement)s',
                                        instruction.mnemonic())))

            if instruction.operands() is not None:
                operands = self._fmt_operands(instruction.operands())
                row.add_cell(Cell(operands))
            else:
                row.add_cell(Cell())

            table.add_row(row)

        table.draw(terminal, width)
