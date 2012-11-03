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

from ..parameter import Parameter
from ..parameter import ParameterBoolean
from ..parameter import register_parameter
from .voidwalker import VoidwalkerParameter


@register_parameter
class ShowParameter(Parameter):
    show_doc = '(void)walker show parameters'

    def __init__(self):
        super(ShowParameter, self).__init__()

    def default_value(self):
        return None

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerParameter.name(), 'show')


@register_parameter
class ShowRegistersParameter(ParameterBoolean):
    show_doc = 'Show registers is set to'

    def __init__(self):
        super(ShowRegistersParameter, self).__init__()

    def default_value(self):
        return True

    @staticmethod
    def name():
        return '%s %s' % (ShowParameter.name(), 'registers')


@register_parameter
class ShowStackParameter(ParameterBoolean):
    show_doc = 'Show stack is set to'

    def __init__(self):
        super(ShowStackParameter, self).__init__()

    def default_value(self):
        return True

    @staticmethod
    def name():
        return '%s %s' % (ShowParameter.name(), 'stack')


@register_parameter
class ShowInstructionsParameter(ParameterBoolean):
    show_doc = 'Show instructions is set to'

    def __init__(self):
        super(ShowInstructionsParameter, self).__init__()

    def default_value(self):
        return True

    @staticmethod
    def name():
        return '%s %s' % (ShowParameter.name(), 'instructions')
