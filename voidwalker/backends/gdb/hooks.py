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

from ...framework.interface.command import StackCommand
from ...framework.interface.command import register_command
from ...framework.interface.parameter import BooleanParameter
from ...framework.interface.parameter import PrefixParameter
from ...framework.interface.parameter import register_parameter

from ...application.commands.context import ContextCommand
from ...application.commands.voidwalker import VoidwalkerCommand
from ...application.parameters.voidwalker import VoidwalkerParameter


@register_parameter
class HookParameter(PrefixParameter):
    '''(void)walker hook parameters'''

    def __init__(self):
        super(HookParameter, self).__init__()

    def default_value(self):
        return None

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerParameter.name(), 'hook')


@register_parameter
class ContextHookParameter(BooleanParameter):
    '''Dump context when relevant hooks are called'''

    DEFAULT_VALUE = True

    def __init__(self):
        super(ContextHookParameter, self).__init__()

    @staticmethod
    def name():
        return '%s %s' % (HookParameter.name(), 'context')

    def default_value(self):
        return self.DEFAULT_VALUE


@register_command
class VoidwalkerHookStop(StackCommand):
    '''This command should be called from GDB hook-stop.

To support all features of (void)walker this command must be called from GDB's
hook-stop command. If you haven't defined hook-stop simply add the following
to your ~/.gdbinit:

    define hook-stop
        voidwalker hook-stop
    end'''

    def __init__(self):
        super(VoidwalkerHookStop, self).__init__()
        self._terminal = None

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'hook-stop')

    def execute(self, config, *_):
        context_hook_name = ContextHookParameter.name()
        if config.parameter(context_hook_name).value():
            gdb.execute(ContextCommand.name())
