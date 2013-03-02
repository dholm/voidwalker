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

from flowui.terminal import AnsiTerminal
from flowui.terminals import SysTerminal
from flowui.themes import Solarized
from unittest import TestCase

from framework.interface.command import Command
from framework.interface.command import CommandBuilder
from framework.interface.command import DataCommand
from framework.interface.command import register_command
from framework.interface.config import Configuration
from framework.interface.parameter import BooleanParameter
from framework.interface.parameter import EnumParameter
from framework.interface.parameter import Parameter
from framework.interface.parameter import ParameterBuilder
from framework.interface.parameter import register_parameter

from backends.test.interface import TestCommandFactory
from backends.test.interface import TestParameterFactory


@register_command
class TestCommand(Command):
    @staticmethod
    def name():
        return 'test'


@register_command
class TestDataCommand(DataCommand):
    @staticmethod
    def name():
        return '%s %s' % (TestCommand.name(), 'data')


class CommandTest(TestCase):
    def setUp(self):
        self._terminal = AnsiTerminal(SysTerminal(), Solarized())

    def test_command(self):
        bldr = CommandBuilder(TestCommandFactory(), Configuration(),
                              self._terminal)

        self.assertIsNotNone(bldr.command(TestCommand.name()))
        self.assertIsNotNone(bldr.command(TestDataCommand.name()))


@register_parameter
class TestParameter(Parameter):
    '''test parameter'''

    def init(self):
        pass

    def default_value(self):
        return None

    @staticmethod
    def name():
        return 'test'


@register_parameter
class BooleanParameterTest(BooleanParameter):
    '''test boolean parameter'''

    def default_value(self):
        return True

    @staticmethod
    def name():
        return '%s %s' % (TestParameter.name(), 'boolean')


@register_parameter
class EnumParameterTest(EnumParameter):
    '''test enum parameter'''

    values = ['alpha', 'beta', 'gamma']

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
        config = Configuration()
        ParameterBuilder(TestParameterFactory(), config)
        self._config = config

    def test_parameter(self):
        name = TestParameter.name()
        self.assertIsNotNone(self._config.parameter(name))

    def test_boolean_parameter(self):
        name = BooleanParameterTest.name()
        self.assertIsNotNone(self._config.parameter(name))

    def test_enum_parameter(self):
        name = EnumParameterTest.name()
        self.assertIsNotNone(self._config.parameter(name))
