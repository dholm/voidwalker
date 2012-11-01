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

from ...ui.theme import ThemeManager
from ..parameter import ParameterEnum
from ..parameter import register_parameter


@register_parameter
class ThemeParameter(ParameterEnum):
    DEFAULT_VALUE = 'solarized'

    show_doc = 'Voidwalker\'s theme is currently set to'

    def __init__(self):
        self._themes = [x for x in ThemeManager().themes()]
        super(ThemeParameter, self).__init__()

    def default_value(self):
        return self.DEFAULT_VALUE

    def init(self):
        pass

    def sequence(self):
        return self._themes

    @staticmethod
    def name():
        return '%s' % ('voidwalker-theme')
