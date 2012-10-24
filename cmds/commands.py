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
from base.decorators import singleton

@singleton
class CommandManager(object):
    _commands = {}
    _instances = {}

    def init(self, inferior_manager, terminal):
        for name, command in self._commands.iteritems():
            self._instances[name] = command(inferior_manager, terminal)

    def add_command(self, command):
        self._commands[command.name()] = command

def gdb_register_command(cls):
    CommandManager().add_command(cls)
    return cls
