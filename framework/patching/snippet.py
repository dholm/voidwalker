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

from ..utils.decorators import singleton


@singleton
class SnippetManager(object):
    def __init__(self):
        self._snippets = {}

    def add_snippet(self, cls):
        snippet = cls()
        self._snippets[snippet.name()] = snippet

    def snippet(self, name):
        assert name in self._snippets
        return self._snippets[name]

    def snippets(self):
        return self._snippets.iteritems()


def register_snippet(cls):
    SnippetManager().add_snippet(cls)
    return cls


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
