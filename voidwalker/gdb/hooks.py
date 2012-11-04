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
from ..interface.command import register_command
from ..interface.commands.context import ContextCommand
from ..interface.commands.voidwalker import VoidwalkerCommand


@register_command
class VoidwalkerHookStop(Command):
    def __init__(self):
        super(VoidwalkerHookStop, self).__init__()
        self._terminal = None

    def init(self, terminal):
        self._terminal = terminal

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'hook-stop')

    def invoke(self, inferior, argument):
        gdb.execute(ContextCommand.name())