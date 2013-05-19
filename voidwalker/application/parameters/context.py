# (void)walker configuration parameters
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from ...framework.interface.parameter import PrefixParameter
from ...framework.interface.parameter import IntegerParameter
from ...framework.interface.parameter import register_parameter

from .voidwalker import VoidwalkerParameter


@register_parameter
class ContextParameter(PrefixParameter):
    '''(void)walker context command parameters'''

    def __init__(self):
        super(ContextParameter, self).__init__()

    def default_value(self):
        return None

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerParameter.name(), 'context')


@register_parameter
class ContextStackParameter(IntegerParameter):
    '''Number of doublewords of stack

Controls the number of doublewords of stack to include in each context.'''

    DEFAULT_VALUE = 8

    show_doc = 'Number of doublewords of stack to show is set to'

    def __init__(self):
        super(ContextStackParameter, self).__init__()

    def default_value(self):
        return self.DEFAULT_VALUE

    @staticmethod
    def name():
        return '%s %s' % (ContextParameter.name(), 'stackdw')


@register_parameter
class ContextInstructionsParameter(IntegerParameter):
    '''Number of instructions

The total number of instructions to include in each context.'''

    DEFAULT_VALUE = 6

    show_doc = 'Number of instructions to show is set to'

    def __init__(self):
        super(ContextInstructionsParameter, self).__init__()

    def default_value(self):
        return self.DEFAULT_VALUE

    @staticmethod
    def name():
        return '%s %s' % (ContextParameter.name(), 'instructions')
