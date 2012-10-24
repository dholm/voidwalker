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

import re

from base.decorators import singleton

class Theme(object):
    _default_fg = None
    _default_bg = None
    _faces = None
    _ansi_escape_expression = re.compile((r'\x1B\[((\d+|"[^"]*")'
                                          r'(;(\d+|"[^"]*"))*)?'
                                          r'[A-Za-z]'))

    def _add_face(self, face, fg=None, bg=None):
        if not fg:
            fg = self._default_fg
        if not bg:
            bg = self._default_bg

        self._faces[face] = '%s%s' % (fg, bg)

    def __init__(self, default_foreground, default_background):
        self._default_fg = default_foreground
        self._default_bg = default_background
        self._faces = {'face-none': '\x1b[0m',
                       'face-bold': '\x1b[1m',
                       'face-italic': '\x1b[2m',
                       'face-underline': '\x1b[4m'}
        self._add_face('face-default', default_foreground, default_background)

    def reset(self):
        return self._faces['face-none']

    def len(self, string, format_dictionary=None):
        d = self._faces
        if format_dictionary:
            d.update(format_dictionary)

        return len(self._ansi_escape_expression.sub('', (string % d)))

    def write(self, string, format_dictionary=None):
        d = self._faces
        if format_dictionary:
            d.update(format_dictionary)

        return (self._faces['face-default'] + (string % d))
