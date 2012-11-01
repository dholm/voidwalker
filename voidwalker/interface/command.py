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

from ..utils.decorators import singleton


class Command(object):
    def init(self, terminal):
        raise NotImplementedError


class DataCommand(Command):
    pass


class CommandFactory(object):
    def create_command(self, command_type):
        raise NotImplementedError


@singleton
class CommandManager(object):
    def __init__(self):
        self._commands = {}
        self._instances = {}

    def init(self, command_factory, terminal):
        for name, Cmd in self._commands.iteritems():
            self._instances[name] = command_factory.create_command(Cmd)
            self._instances[name].init(terminal)

    def add_command(self, command):
        self._commands[command.name()] = command


def register_command(cls):
    CommandManager().add_command(cls)
    return cls
