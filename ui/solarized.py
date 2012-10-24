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

from theme import Theme

class Solarized(Theme):
    _background256 = '\x1b[48;5;%dm'
    _foreground256 = '\x1b[38;5;%dm'
    _colors256 = [234, 235, 240, 241, 244, 245, 254, 230, 136, 166, 160, 125,
                  61, 33, 37, 64]

    _labels = ['base03', 'base02', 'base01', 'base00', 'base0', 'base1',
               'base2', 'base3', 'yellow', 'orange', 'red', 'magenta', 'violet',
               'blue', 'cyan', 'green']
    _colors = {}

    def __init__(self):
        assert len(self._labels) == len(self._colors256)
        colors = dict(zip(self._labels, self._colors256))
        for label, color in colors.items():
            self._colors['fg-' + label] = self._foreground256 % color
            self._colors['bg-' + label] = self._background256 % color

        super(Solarized, self).__init__(self._colors['fg-base0'],
                                        self._colors['bg-base03'])

        self._add_face('face-header',
                       self._colors['fg-base0'], self._colors['bg-base02'])
        self._add_face('face-keyword', fg=self._colors['fg-green'])
        self._add_face('face-special-keyword', fg=self._colors['fg-red'])
        self._add_face('face-constant', fg=self._colors['fg-cyan'])
        self._add_face('face-type', fg=self._colors['fg-yellow'])
        self._add_face('face-comment', fg=self._colors['fg-base01'])
        self._add_face('face-emphasized', fg=self._colors['fg-violet'])


    @staticmethod
    def name():
        return 'solarized'
