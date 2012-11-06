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

from ...target.inferior import InferiorManager
from ...types.data import DataChunk
from ...types.data import DataWidget
from ...ui.widgets import Section
from ..command import DataCommand
from ..command import register_command
from .voidwalker import VoidwalkerCommand


@register_command
class DataDumpCommand(DataCommand):
    '''Dump data: <address> <length>

Dumps data starting from the specified address. The output is shown using the
data widget which displays it in hexadecimal and ascii form (when possible).'''

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'dump')

    def init(self, terminal):
        self._terminal = terminal

    def __init__(self):
        super(DataDumpCommand, self).__init__()
        self._terminal = None

    def invoke(self, thread, arguments, from_tty=False):
        if len(arguments) != 2:
            self._terminal.write(('%(face-error)sError:'
                                  '%(face-normal)s invalid arguments!\n'))
            return

        address = abs(long(arguments[0]))
        size = abs(long(arguments[1]))

        inferior = InferiorManager().inferior(thread.inferior_id())
        data_dump = inferior.read_memory(address, size)
        data_chunk = DataChunk(address, data_dump)

        section = Section('0x%016lX' % address)
        section.add_component(DataWidget(data_chunk))
        section.draw(self._terminal, self._terminal.width())
