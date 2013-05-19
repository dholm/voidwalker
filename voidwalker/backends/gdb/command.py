# (void)walker GDB backend
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from functools import partial

from ...framework.interface import BreakpointCommand
from ...framework.interface import Command
from ...framework.interface import CommandFactory
from ...framework.interface import DataCommand
from ...framework.interface import PrefixCommand
from ...framework.interface import StackCommand
from ...framework.interface import SupportCommand


def get_current_inferior(inferior_repository, inferior_factory):
    inferior_num = gdb.selected_inferior().num
    if not inferior_repository.has_inferior(inferior_num):
        inferior = inferior_factory.create_inferior(inferior_num)
        inferior_repository.add_inferior(inferior)

    return inferior_repository.get_inferior(inferior_num)


def get_current_thread(inferior_repository, inferior_factory,
                       thread_factory):
    if gdb.selected_thread() is not None:
        thread_num = gdb.selected_thread().num

        inferior = get_current_inferior(inferior_repository, inferior_factory)
        if not inferior.has_thread(thread_num):
            thread_factory.create_thread(inferior, thread_num)

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
    def create_data_command(self, command_type, terminal, inferior_repo,
                            inferior_factory, thread_factory):
        class GdbDataCommand(gdb.Command, command_type):
            __doc__ = command_type.__doc__

            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_DATA, gdb.COMPLETE_NONE)

            def invoke(self, argument, _):
                thread = get_current_thread(inferior_repo, inferior_factory,
                                            thread_factory)
                if thread is not None:
                    args = parse_argument_list(argument)
                    command_type.execute(self, terminal, thread, args)

        return GdbDataCommand()

    def create_stack_command(self, command_type, config, terminal,
                             inferior_repo, platform_factory, inferior_factory,
                             thread_factory):
        class GdbStackCommand(gdb.Command, command_type):
            __doc__ = command_type.__doc__

            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_STACK, gdb.COMPLETE_NONE)

            def invoke(self, argument, _):
                thread = get_current_thread(inferior_repo, inferior_factory,
                                            thread_factory)
                if thread is not None:
                    args = parse_argument_list(argument)
                    command_type.execute(self, config, terminal, thread,
                                         platform_factory, args)

        return GdbStackCommand()

    def create_prefix_command(self, command_type, _):
        class GdbPrefixCommand(gdb.Command, command_type):
            __doc__ = command_type.__doc__

            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_USER,
                                     gdb.COMPLETE_COMMAND, True)

        return GdbPrefixCommand()

    def create_support_command(self, command_type, terminal):
        class GdbSupportCommand(gdb.Command, command_type):
            __doc__ = command_type.__doc__

            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_SUPPORT,
                                     gdb.COMPLETE_NONE, True)

            def invoke(self, argument, _):
                args = parse_argument_list(argument)
                command_type.execute(self, terminal, args)

        return GdbSupportCommand()

    def create_brkp_command(self, command_type, terminal, inferior_repo):
        class GdbBreakpointCommand(gdb.Command, command_type):
            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_BREAKPOINTS,
                                     gdb.COMPLETE_NONE)

            def invoke(self, argument, _):
                inferior = get_current_inferior(inferior_repo)
                if inferior is not None:
                    args = parse_argument_list(argument)
                    command_type.execute(self, terminal, inferior, args)

        return GdbBreakpointCommand()

    def create_generic_command(self, command_type):
        class GdbCommand(gdb.Command, command_type):
            __doc__ = command_type.__doc__

            def __init__(self):
                command_type.__init__(self)
                gdb.Command.__init__(self, command_type.name(),
                                     gdb.COMMAND_USER,
                                     gdb.COMPLETE_COMMAND)

        return GdbCommand()

    def create(self, command_type, inferior_repository, platform_factory,
               inferior_factory, thread_factory, config, terminal):
        create_method = [(DataCommand, partial(self.create_data_command,
                                               command_type, terminal,
                                               inferior_repository,
                                               inferior_factory,
                                               thread_factory)),
                         (StackCommand, partial(self.create_stack_command,
                                                command_type, config, terminal,
                                                inferior_repository,
                                                platform_factory,
                                                inferior_factory,
                                                thread_factory)),
                         (PrefixCommand, partial(self.create_prefix_command,
                                                 command_type, terminal)),
                         (SupportCommand, partial(self.create_support_command,
                                                  command_type, terminal)),
                         (BreakpointCommand, partial(self.create_brkp_command,
                                                     command_type, terminal,
                                                     inferior_repository)),
                         (Command, partial(self.create_generic_command,
                                           command_type))]
        for ctype, create in create_method:
            if issubclass(command_type, ctype):
                return create()
        else:
            raise TypeError('Command %s of type %s unknown!' %
                            (command_type.name(), repr(command_type)))
