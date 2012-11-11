# (void)walker unit tests
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

from unittest import TestCase

from framework.interface.command import Command
from framework.interface.command import CommandFactory
from framework.interface.command import CommandManager
from framework.interface.command import DataCommand
from framework.interface.command import register_command
from framework.interface.parameter import Parameter
from framework.interface.parameter import ParameterBoolean
from framework.interface.parameter import ParameterEnum
from framework.interface.parameter import ParameterFactory
from framework.interface.parameter import ParameterManager
from framework.interface.parameter import register_parameter
from framework.utils.decorators import singleton_implementation

from backends.test.terminal import SysTerminal

from .target import TestInferior


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


@register_command
class TestCommand(Command):
    def __init__(self):
        self._terminal = None

    @staticmethod
    def name():
        return 'test'

    def init(self, terminal):
        self._terminal = terminal


@register_command
class TestDataCommand(DataCommand):
    def __init__(self):
        self._terminal = None

    @staticmethod
    def name():
        return '%s %s' % (TestCommand.name(), 'data')

    def init(self, terminal):
        self._terminal = terminal


class CommandTest(TestCase):
    def setUp(self):
        self._terminal = SysTerminal()

    def test_command(self):
        CommandManager().init(self._terminal)

        self.assertIsNotNone(CommandManager().command(TestCommand.name()))
        self.assertIsNotNone(CommandManager().command(TestDataCommand.name()))


@singleton_implementation(ParameterFactory)
class TestParameterFactory(object):
    def create_parameter(self, parameter_type):
        if issubclass(parameter_type, ParameterEnum):
            class TestParameterEnum(parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)
                    self.value = parameter_type.default_value(self)

            return TestParameterEnum()

        elif issubclass(parameter_type, ParameterBoolean):
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


@register_parameter
class TestParameter(Parameter):
    show_doc = 'test parameter'

    def init(self):
        pass

    def default_value(self):
        return None

    @staticmethod
    def name():
        return 'test'


@register_parameter
class TestBooleanParameter(ParameterBoolean):
    show_doc = 'test boolean parameter'

    def default_value(self):
        return True

    @staticmethod
    def name():
        return '%s %s' % (TestParameter.name(), 'boolean')


@register_parameter
class TestEnumParameter(ParameterEnum):
    values = ['alpha', 'beta', 'gamma']
    show_doc = 'test enum parameter'

    def default_value(self):
        return self.values[0]

    def init(self):
        pass

    def sequence(self):
        return self.values

    @staticmethod
    def name():
        return '%s %s' % (TestParameter.name(), 'enum')


class ParameterTest(TestCase):
    def setUp(self):
        ParameterManager().init()

    def test_parameter(self):
        name = TestParameter.name()
        self.assertIsNotNone(ParameterManager().parameter(name))

    def test_boolean_parameter(self):
        name = TestBooleanParameter.name()
        self.assertIsNotNone(ParameterManager().parameter(name))

    def test_enum_parameter(self):
        name = TestEnumParameter.name()
        self.assertIsNotNone(ParameterManager().parameter(name))
