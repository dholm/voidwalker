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

from framework.interface.command import BreakpointCommand
from framework.interface.command import Command
from framework.interface.command import CommandFactory
from framework.interface.command import DataCommand
from framework.interface.command import PrefixCommand
from framework.interface.command import StackCommand
from framework.interface.command import SupportCommand
from framework.target.factory import TargetFactory
from framework.target.inferior import InferiorManager


def get_current_inferior():
    inferior_num = gdb.selected_inferior().num
    inferior = InferiorManager().inferior(inferior_num)
    if not inferior:
        raise gdb.GdbError(('Inferior %d does not exist!' %
                            inferior_num))

    return inferior


def get_current_thread():
    if gdb.selected_thread() is not None:
        thread_num = gdb.selected_thread().num

        inferior = get_current_inferior()
        if not inferior.has_thread(thread_num):
            TargetFactory().create_thread(inferior, thread_num)

        if inferior.has_thread(thread_num):
            return inferior.thread(thread_num)

    return None


def parse_argument_list(argument):
    args = []
    for obj in gdb.string_to_argv(argument):
        try:
            obj = gdb.parse_and_eval('%s' % obj)
        except gdb.error:
            pass

        args.append(obj)
    return args


class GdbCommandFactory(CommandFactory, object):
    def create_command(self, command_type):
        if issubclass(command_type, DataCommand):
            class GdbDataCommand(gdb.Command, command_type):
                __doc__ = command_type.__doc__

                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_DATA, gdb.COMPLETE_NONE)

                def invoke(self, argument, from_tty):
                    thread = get_current_thread()
                    if thread is not None:
                        args = parse_argument_list(argument)
                        command_type.invoke(self, thread, args, from_tty)

            return GdbDataCommand()

        if issubclass(command_type, StackCommand):
            class GdbStackCommand(gdb.Command, command_type):
                __doc__ = command_type.__doc__

                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_STACK, gdb.COMPLETE_NONE)

                def invoke(self, argument, from_tty):
                    thread = get_current_thread()
                    if thread is not None:
                        args = parse_argument_list(argument)
                        command_type.invoke(self, thread, args, from_tty)

            return GdbStackCommand()

        if issubclass(command_type, PrefixCommand):
            class GdbPrefixCommand(gdb.Command, command_type):
                __doc__ = command_type.__doc__

                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_USER,
                                         gdb.COMPLETE_COMMAND, True)
                    self._terminal = None

            return GdbPrefixCommand()

        if issubclass(command_type, SupportCommand):
            class GdbSupportCommand(gdb.Command, command_type):
                __doc__ = command_type.__doc__

                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_SUPPORT,
                                         gdb.COMPLETE_NONE, True)

            return GdbSupportCommand()

        if issubclass(command_type, BreakpointCommand):
            class GdbBreakpointCommand(gdb.Command, command_type):
                def __init__(self):
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_BREAKPOINTS,
                                         gdb.COMPLETE_NONE)

                def invoke(self, argument, from_tty):
                    inferior = get_current_inferior()
                    if inferior is not None:
                        args = parse_argument_list(argument)
                        command_type.invoke(self, inferior, args, from_tty)

            return GdbBreakpointCommand()

        if issubclass(command_type, Command):
            class GdbCommand(gdb.Command, command_type):
                __doc__ = command_type.__doc__

                def __init__(self):
                    command_type.__init__(self)
                    gdb.Command.__init__(self, command_type.name(),
                                         gdb.COMMAND_USER,
                                         gdb.COMPLETE_COMMAND)

            return GdbCommand()

        else:
            raise TypeError('Command type %s unknown!' %
                            str(command_type))
