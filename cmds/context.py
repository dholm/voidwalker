# (void)walker command interface
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

from arch.context import Context
from ui.widgets import Section
from ui.widgets import Table

from commands import gdb_register_command

@gdb_register_command
class ContextCommand(gdb.Command):
    _inferior_manager = None
    _terminal = None

    _register_fmt = {16: '0x%032lX',
                     8: '0x%016lX',
                     4: '0x%08lX',
                     2: '0x%04lX'}

    @staticmethod
    def name():
        return 'pcontext'

    def __init__(self, inferior_manager, terminal):
        super(ContextCommand, self).__init__(self.name(),
                                             gdb.COMMAND_DATA,
                                             gdb.COMPLETE_NONE)

        self._inferior_manager = inferior_manager
        self._terminal = terminal

    def _print_regs(self, cpu):
        table = Table()
        reg_size = 0
        for name, register in cpu.registers():
            reg_size = max(reg_size, len(name))

        for name, register in cpu.registers():
            contents = ('%(face-keyword)s' +
                        (('%%-%ds: ' % reg_size) % register.name()))

            size = register.size()
            value = register.value()
            if value:
                contents += ('%(face-constant)s' +
                             (self._register_fmt[size] % value))
            else:
                contents += ('%(face-comment)s' +
                             ' %(dashes)s ' % {'dashes': '-' * size * 2})

            cell = Table.Cell(contents)
            table.add_cell(cell)

        section = Section('regs')
        section.add_component(table)
        section.draw(self._terminal, self._terminal.width())

    def invoke(self, argument, from_tty):
        inferior_num = gdb.selected_inferior().num
        inferior = self._inferior_manager().get_inferior(inferior_num)
        if not inferior:
            raise gdb.GdbError(('Inferior %d does not exist in manager!' %
                                inferior_num))

        self._print_regs(inferior.cpu())
        end_section = Section(None)
        end_section.draw(self._terminal, self._terminal.width())
        self._terminal.reset()
