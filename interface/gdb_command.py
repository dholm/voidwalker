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

import gdb

from base.gdb_inferiors import InferiorManager
from interface.commands import Command
from interface.commands import DataCommand


def factory(command_type):
    if DataCommand in command_type.__bases__:
        class GdbDataCommand(gdb.Command, command_type):
            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_DATA, gdb.COMPLETE_NONE)

            def invoke(self, argument, from_tty):
                inferior_num = gdb.selected_inferior().num
                inferior = InferiorManager().get_inferior(inferior_num)
                if not inferior:
                    raise gdb.GdbError(('Inferior %d does not exist!' %
                                        inferior_num))

                command_type.invoke(self, inferior, argument)

        return GdbDataCommand()

    elif Command in command_type.__bases__:
        class GdbCommand(gdb.Command, command_type):
            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_USER, gdb.COMPLETE_COMMAND,
                                     True)

        return GdbCommand()

    else:
        raise TypeError('Command type %s unknown!' %
                        str(command_type))
