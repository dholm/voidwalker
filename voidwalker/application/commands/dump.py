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

from flowui.widgets import Section

from ...framework.interface.command import DataCommand
from ...framework.interface.command import PrefixCommand
from ...framework.interface.command import register_command
from ...framework.types.data import DataChunk
from ...framework.types.data import DataWidget
from ...framework.types.instructions import InstructionListingWidget

from .voidwalker import VoidwalkerCommand


@register_command
class DumpCommand(PrefixCommand):
    '''Commands for dumping data'''

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'dump')

    def __init__(self):
        super(DumpCommand, self).__init__()


@register_command
class DumpDataCommand(DataCommand):
    '''Dump data: <address> <length>

Dumps data starting from the specified address. The output is shown using the
data widget which displays it in hexadecimal and ascii form (when possible).'''

    @staticmethod
    def name():
        return '%s %s' % (DumpCommand.name(), 'data')

    def __init__(self):
        super(DumpDataCommand, self).__init__()

    def execute(self, terminal, thread, arguments):
        if len(arguments) != 2:
            terminal.write(('%(face-error)sError:'
                            '%(face-normal)s invalid arguments!\n'))
            return

        address = abs(long(arguments[0]))
        size = abs(long(arguments[1]))

        inferior = thread.get_inferior()
        data_dump = inferior.read_memory(address, size)
        data_chunk = DataChunk(address, data_dump)

        section = Section('0x%016lX' % address)
        section.add_component(DataWidget(data_chunk))
        section.draw(terminal, terminal.width())


@register_command
class DumpInstructionsCommand(DataCommand):
    '''Dump instructions: <address> <length>

Dump disassembly starting from the specified address. The output is shown
using the instruction listing widget and perform syntax highlighting on the
output.'''

    @staticmethod
    def name():
        return '%s %s' % (DumpCommand.name(), 'instructions')

    def __init__(self):
        super(DumpInstructionsCommand, self).__init__()

    def execute(self, terminal, thread, arguments):
        if len(arguments) != 2:
            terminal.write(('%(face-error)sError:'
                            '%(face-normal)s invalid arguments!\n'))
            return

        address = abs(long(arguments[0]))
        size = abs(long(arguments[1]))

        inferior = thread.get_inferior()
        listing = inferior.disassemble(address, size)

        section = Section('0x%016lX' % address)
        section.add_component(InstructionListingWidget(listing))
        section.draw(terminal, terminal.width())
