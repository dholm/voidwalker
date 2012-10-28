#!/usr/bin/env python

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

import sys
import unittest

import interface
import ui
import tests


def parameter_factory(parameter_type):
    parameter = parameter_type()
    parameter.value = parameter.default_value()
    return parameter

interface.parameters.ParameterManager().init(parameter_factory)
terminal = ui.terminal.SysTerminal()
ui.theme.ThemeManager().init(terminal.depth())

suite = tests.suite()
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit({True: 0, False: 3}[result.wasSuccessful()])
