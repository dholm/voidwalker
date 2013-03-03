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

from framework.interface import BooleanParameter
from framework.interface import CommandBuilder
from framework.interface import Configuration
from framework.interface import DataCommand
from framework.interface import EnumParameter
from framework.interface import Parameter
from framework.interface import ParameterBuilder
from framework.interface import PrefixCommand
from framework.interface import register_command
from framework.interface import register_parameter
from framework.platform import CpuFactory
from framework.target import InferiorRepository

from backends.test import TestCommandFactory
from backends.test import TestParameterFactory
from backends.test import TestPlatformFactory
from backends.test import TestTargetFactory


@register_command
class TestCommand(PrefixCommand):
    @staticmethod
    def name():
        return 'test'


@register_command
class TestDataCommand(DataCommand):
    @staticmethod
    def name():
        return '%s %s' % (TestCommand.name(), 'data')

    def execute(self, terminal, thread, argument):
        pass


class CommandTest(TestCase):
    def setUp(self):
        self._terminal = AnsiTerminal(SysTerminal(), Solarized())

    def test_command(self):
        platform_factory = TestPlatformFactory()
        target_factory = TestTargetFactory(CpuFactory(platform_factory))
        inferior_repository = InferiorRepository(target_factory)
        bldr = CommandBuilder(TestCommandFactory(), inferior_repository,
                              platform_factory, target_factory,
                              Configuration(), self._terminal)

        self.assertIn(TestCommand.name(), bldr.commands)
        self.assertIn(TestDataCommand.name(), bldr.commands)


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
