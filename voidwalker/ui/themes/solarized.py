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
class Solarized(Theme):
    _color_map = {8: [(0, 'bold'), 0, (2, 'bold'), (3, 'bold'), (4, 'bold'),
                      (6, 'bold'), 7, (7, 'bold'), 3, (1, 'bold'), 1, 5,
                      (5, 'bold'), 4, 6, 2],

                  16: [8, 0, 10, 11, 12, 14, 7, 15, 3, 9, 1, 5, 13, 4, 6, 2],

                  256: [234, 235, 240, 241, 244, 245, 254, 230, 136, 166, 160,
                        125, 61, 33, 37, 64]}

    _labels = ('base03 base02 base01 base00 base0 base1 base2 base3 yellow '
               'orange red magenta violet blue cyan green').split()

    def __init__(self, depth):
        assert len(self._labels) == len(self._color_map.get(depth, 8))
        colors = dict(zip(self._labels,
                          [x if type(x) == tuple else (x, 'normal')
                           for x in self._color_map.get(depth, 8)]))

        default_bg = colors['base03'][0]
        default = self._color(depth, colors['base0'][0], default_bg,
                              colors['base0'][1])
        super(Solarized, self).__init__(default)

        normal = self._color(depth, colors['base0'][0], default_bg,
                             colors['base0'][1])
        self._add_face('normal', normal)
        comment = self._color(depth, colors['base01'][0], default_bg, 'italic')
        self._add_face('comment', comment)
        constant = self._color(depth, colors['cyan'][0], default_bg,
                               colors['cyan'][1])
        self._add_face('constant', constant)
        identifier = self._color(depth, colors['blue'][0], default_bg,
                                 colors['blue'][1])
        self._add_face('identifier', identifier)
        statement = self._color(depth, colors['green'][0], default_bg,
                                colors['green'][1])
        self._add_face('statement', statement)
        preproc = self._color(depth, colors['orange'][0], default_bg,
                              colors['orange'][1])
        self._add_face('preproc', preproc)
        tp = self._color(depth, colors['yellow'][0], default_bg,
                         colors['yellow'][1])
        self._add_face('type', tp)
        special = self._color(depth, colors['red'][0], default_bg,
                              colors['red'][1])
        self._add_face('special', special)
        underlined = self._color(depth, colors['violet'][0], default_bg,
                                 colors['violet'][1])
        self._add_face('underlined', underlined)
        error = self._color(depth, colors['red'][0], default_bg,
                            colors['red'][1])
        self._add_face('error', error, 'bold')
        todo = self._color(depth, colors['magenta'][0], default_bg,
                           colors['magenta'][1])
        self._add_face('todo', todo, 'bold')

        header = self._color(depth, colors['base1'][0], colors['base02'][0],
                             colors['base1'][1])
        self._add_face('header', header)

    @staticmethod
    def name():
        return 'solarized'
