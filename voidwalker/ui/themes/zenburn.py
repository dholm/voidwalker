# (void)walker user interface
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

from ..theme import Theme
from ..theme import register_theme


@register_theme
class Zenburn(Theme):
    def __init__(self, depth):
        default_bg = 237
        super(Zenburn, self).__init__(self._color(depth, 188, default_bg))

        self._add_face('comment', self._color(depth, 108, default_bg))
        self._add_face('constant', self._color(depth, 181, default_bg, 'bold'))
        self._add_face('identifier', self._color(depth, 223, default_bg))
        self._add_face('statement', self._color(depth, 187, 234))
        self._add_face('preproc', self._color(depth, 223, default_bg, 'bold'))
        self._add_face('type', self._color(depth, 187, default_bg))
        self._add_face('special', self._color(depth, 181, default_bg))
        self._add_face('underlined', self._color(depth, 188, 234, 'bold'))
        self._add_face('error', self._color(depth, 115, 236, 'bold'))
        self._add_face('todo', self._color(depth, 108, 234, 'bold'))

        self._add_face('header', self._color(depth, 108, 235))

    @staticmethod
    def name():
        return 'zenburn'
