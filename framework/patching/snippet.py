# (void)walker code snippet support
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


class SnippetRepository(object):
    def snippet(self, name):
        assert name in _snippet_map
        return _snippet_map[name]

    def snippets(self):
        return _snippet_map.items()


def register_snippet(cls):
    _snippet_map[cls.name()] = cls()
    return cls

_snippet_map = {}


class Snippet(object):
    def architectures(self):
        raise NotImplementedError

    def implementation(self, architecture):
        raise NotImplementedError

    @staticmethod
    def description():
        raise NotImplementedError

    @staticmethod
    def name():
        raise NotImplementedError
