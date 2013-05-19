# (void)walker configuration parameters
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

from ...framework.interface.parameter import PrefixParameter
from ...framework.interface.parameter import register_parameter


@register_parameter
class VoidwalkerParameter(PrefixParameter):
    '''(void)walker parameters'''

    def __init__(self):
        super(VoidwalkerParameter, self).__init__()

    def init(self):
        pass

    def default_value(self):
        return None

    @staticmethod
    def name():
        return 'voidwalker'
