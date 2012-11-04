# (void)walker GDB backend
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

from ..interface.command import Command
from ..interface.command import CommandFactory
from ..interface.command import DataCommand
from ..target.factory import TargetFactory
from ..target.inferior import InferiorManager
from ..utils.decorators import singleton_implementation


def get_current_thread():
    inferior_num = gdb.selected_inferior().num
    inferior = InferiorManager().inferior(inferior_num)
    if not inferior:
        raise gdb.GdbError(('Inferior %d does not exist!' %
                            inferior_num))

    if gdb.selected_thread() is not None:
        thread_num = gdb.selected_thread().num
        if not inferior.has_thread(thread_num):
            TargetFactory().create_thread(inferior, thread_num)

        if inferior.has_thread(thread_num):
            return inferior.thread(thread_num)

    return None


@singleton_implementation(CommandFactory)
class GdbCommandFactory(object):
    def create_command(self, command_type):
        if issubclass(command_type, DataCommand):
            class GdbDataCommand(gdb.Command, command_type):
                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_DATA, gdb.COMPLETE_NONE)

                def invoke(self, argument, from_tty):
                    thread = get_current_thread()
                    if thread is not None:
                        command_type.invoke(self, thread, argument, from_tty)

            return GdbDataCommand()

        if issubclass(command_type, Command):
            class GdbCommand(gdb.Command, command_type):
                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_USER,
                                         gdb.COMPLETE_COMMAND, True)

            return GdbCommand()

        else:
            raise TypeError('Command type %s unknown!' %
                            str(command_type))
