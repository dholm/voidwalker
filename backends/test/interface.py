# (void)walker unit test backend
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

from framework.interface.command import Command
from framework.interface.command import CommandFactory
from framework.interface.command import DataCommand
from framework.interface.command import register_command
from framework.interface.parameter import BooleanParameter
from framework.interface.parameter import EnumParameter
from framework.interface.parameter import Parameter
from framework.interface.parameter import ParameterFactory
from framework.utils.decorators import singleton_implementation

from .target import TestInferior


@register_command
class TestCommand(Command):
    def __init__(self):
        self._terminal = None

    @staticmethod
    def name():
        return 'test'


@register_command
class TestDataCommand(DataCommand):
    def __init__(self):
        self._terminal = None

    @staticmethod
    def name():
        return '%s %s' % (TestCommand.name(), 'data')


@singleton_implementation(CommandFactory)
class TestCommandFactory(object):
    def create_command(self, command_type):
        if issubclass(command_type, DataCommand):
            class TestDataCommand(command_type):
                def __init__(self):
                    command_type.__init__(self)

                def invoke(self, argument, from_tty):
                    inferior = TestInferior()
                    command_type.invoke(self, inferior, argument)

            return TestDataCommand()

        if issubclass(command_type, Command):
            class TestCommand(command_type):
                def __init__(self):
                    command_type.__init__(self)

            return TestCommand()

        else:
            raise TypeError('Command type %s unknown!' %
                            str(command_type))


@singleton_implementation(ParameterFactory)
class TestParameterFactory(object):
    def create_parameter(self, parameter_type):
        if issubclass(parameter_type, EnumParameter):
            class TestParameterEnum(parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)
                    self.value = parameter_type.default_value(self)

            return TestParameterEnum()

        elif issubclass(parameter_type, BooleanParameter):
            class TestParameterBoolean(parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)
                    self.value = parameter_type.default_value(self)

            return TestParameterBoolean()

        elif issubclass(parameter_type, Parameter):
            class TestParameter(parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)

            return TestParameter()

        else:
            raise TypeError('Parameter type %s unknown!' %
                            str(type(parameter_type)))
