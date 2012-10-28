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
    _ansi_escape_expression = re.compile((r'\x1B\[((\d+|"[^"]*")'
                                          r'(;(\d+|"[^"]*"))*)?'
                                          r'[A-Za-z]'))

    _colors_fmt = {8: '\x1b[%d;3%1d;4%1dm',
                   16: '\x1b[%d;38;5;%d;48;5;%dm',
                   256: '\x1b[%d;38;5;%d;48;5;%dm'}
    _property_fmt = '\x1b[%dm'

    _properties = {'normal': 0,
                   'bold': 1,
                   'italic': 2,
                   'underline': 4}

    """Properties
    normal     - normal face
    bold
    italic
    underline
    """

    """Faces
    face-normal
    face-comment
    face-constant   - string, char, number etc constants
    face-identifier - variable/function name
    face-statement  - statements (if, else, for etc)
    face-define     - definitions (i.e. #define X)
    face-type       - types (integer, static, struct etc)
    face-special    - special symbols or characters
    face-underlined - text that stands out (i.e. links)
    face-error
    face-attention  - anything that needs extra attention

    face-header     - section headers etc
    """

    def _add_face(self, face, color, prop='normal'):
        if prop in self._properties:
            prop = self._properties[prop]

        self._faces['face-' + face] = '%s%s' % (self._property_fmt % prop,
                                                color)

    def _color(self, depth, fg, bg, prop='normal'):
        if prop in self._properties:
            prop = self._properties[prop]
        return (self._colors_fmt.get(depth, 8) %
                (prop, fg, bg))

    def __init__(self, default_color):
        self._default_color = default_color

        self._faces = {}
        self._add_face('normal', default_color)
        self._faces['face-reset'] = self.property('normal')

    def property(self, name):
        assert name in self._properties
        return (self._property_fmt % self._properties[name])

    def faces(self):
        return self._faces

    def face(self, name):
        assert ('face-%s' % name) in self._faces
        return self._faces.get('face-%s' % name, self._faces['face-normal'])

    def _filter_string(self, string):
        string = string.expandtabs()
        return string

    def len(self, string, format_dictionary=None):
        d = self._faces
        if format_dictionary:
            d.update(format_dictionary)

        filtered = self._filter_string(string)
        return len(self._ansi_escape_expression.sub('', (filtered % d)))

    def write(self, string, format_dictionary=None):
        d = self._faces
        if format_dictionary:
            d.update(format_dictionary)

        filtered = self._filter_string(string)
        return '%s%s' % (self.face('normal'), (filtered % d))


@singleton
class ThemeManager(object):
    _themes = {}
    _instances = {}

    def init(self, depth):
        for name, theme in self._themes.iteritems():
            self._instances[name] = theme(depth)

    def themes(self):
        return self._themes.iterkeys()

    def theme(self, name):
        assert name in self._instances
        return self._instances[name]

    def add_theme(self, theme):
        self._themes[theme.name().strip()] = theme


def register_theme(cls):
    ThemeManager().add_theme(cls)
    return cls
