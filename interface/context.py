# (void)walker application interface
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

from base.recipes import grouper
from ui.widgets import Section
from ui.widgets import Table

from interface.commands import DataCommand
from interface.commands import register_command
from interface.gdb_collector import GdbCollectorFactory
from interface.voidwalker import VoidwalkerCommand


@register_command
class ContextCommand(DataCommand):
    _inferior_manager = None
    _terminal = None

    _ascii_filter = ''.join([['.', chr(x)]
                             [chr(x) in string.printable[:-5]]
                             for x in xrange(256)])
    _register_fmt = {16: '0x%032lX',
                     8: '0x%016lX',
                     4: '0x%08lX',
                     2: '0x%04lX'}

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'context')

    def init(self, terminal):
        self._terminal = terminal

    def __init__(self):
        super(ContextCommand, self).__init__()

    def _print_regs(self, context):
        table = Table()
        reg_size = 0
        for name, register in context.registers():
            reg_size = max(reg_size, len(name))

        for name, register in context.registers():
            contents = [('%(face-identifier)s' +
                         (('%%-%ds: ' % reg_size) % name))]

            size = register.size()
            value = register.value()
            if value:
                contents += [('%(face-constant)s' +
                              (self._register_fmt[size] % value))]
            else:
                contents += [('%(face-comment)s' +
                              ' %(dashes)s ' % {'dashes': '-' * size * 2})]

            cell = Table.Cell(''.join(contents))
            table.add_cell(cell)

        section = Section('regs')
        section.add_component(table)
        section.draw(self._terminal, self._terminal.width())

    def _print_stack(self, context):
        table = Table()

        address = context.stack().keys()[0]
        for address, line in context.stack().iteritems():
            hex_string = []
            ascii_string = []
            for octuple in grouper(8, line):
                for quadruple in grouper(4, octuple):
                    hex_string += [(' %02x' % i) for i in quadruple]
                    filtered = ''.join([chr(x).translate(self._ascii_filter)
                                        for x in quadruple])
                    ascii_string += filtered

                hex_string += ['  ']
                ascii_string += ['  ']

            contents = ('0x%016x:    %s    %s' % (address, ''.join(hex_string),
                                                  ''.join(ascii_string)))
            row = Table.Row(contents)
            address += 16
            table.add_row(row)

        section = Section('stack')
        section.add_component(table)
        section.draw(self._terminal, self._terminal.width())

    def _print_instructions(self, context):
        table = Table()
        for instruction in context.instructions():
            face = '%(face-normal)s'
            if instruction['meta']:
                face = '%(face-underlined)s'

            content = []
            content += [('%s%s' % (face, instruction['address']))]
            if instruction['symbol']:
                content += [('   %(face-identifier)s' + instruction['symbol'])]
            content += [('   %s%s' % (face, instruction['mnemonic']))]
            if instruction['operands']:
                content += [('   %s%s' % (face, instruction['operands']))]
            row = Table.Row(''.join(content))
            table.add_row(row)

        section = Section('code')
        section.add_component(table)
        section.draw(self._terminal, self._terminal.width())

    def invoke(self, inferior, argument):
        context = GdbCollectorFactory().create_context(inferior.cpu())

        self._print_regs(context)
        self._print_stack(context)
        self._print_instructions(context)
        end_section = Section(None)
        end_section.draw(self._terminal, self._terminal.width())
        self._terminal.reset()
