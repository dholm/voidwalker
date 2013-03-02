# (void)walker command line interface
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

import abc


class Command(object):
    def __init__(self):
        self._inferior_repository = None
        self._target_factory = None
        self._config = None
        self._terminal = None

    def init(self, inferior_repository, platform_factory, target_factory,
             config, terminal):
        self._platform_factory = platform_factory
        self._inferior_repository = inferior_repository
        self._target_factory = target_factory
        self._config = config
        self._terminal = terminal


class PrefixCommand(Command):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def invoke(self, *_):
        self._terminal.write('%(face-error)sAttempting to invoke an '
                             'incomplete command!\n')


class DataCommand(Command):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def invoke(self, thread, argument, from_tty=False):
        raise NotImplementedError


class StackCommand(Command):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def invoke(self, thread, argument, from_tty=False):
        raise NotImplementedError


class BreakpointCommand(Command):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def invoke(self, inferior, argument, from_tty=False):
        raise NotImplementedError


class SupportCommand(Command):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def invoke(self, argument, from_tty=False):
        raise NotImplementedError


class CommandFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, command_type):
        raise NotImplementedError


class CommandBuilder(object):
    def __init__(self, command_factory, inferior_repository, platform_factory,
                 target_factory, config, terminal):
        self._commands = {}
        for Cmd in _command_list:
            self._commands[Cmd.name()] = command_factory.create(Cmd)
            self._commands[Cmd.name()].init(inferior_repository,
                                            platform_factory, target_factory,
                                            config, terminal)

    def command(self, name):
        assert name in self._commands
        return self._commands[name]


def register_command(cls):
    _command_list.append(cls)
    return cls

_command_list = []
