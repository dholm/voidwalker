# (void)walker unit tests
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

from unittest import TestCase

from framework.patching import SnippetRepository

import application.patching


class SnippetsTest(TestCase):
    def test_snippet_manager(self):
        snippet_repository = SnippetRepository()
        for name, snippet in snippet_repository.snippets():
            print 'Snippet: %s %s' % (name, snippet.description())
            for architecture in snippet.architectures():
                implementation = snippet.implementation(architecture)
                print '\t%s' % implementation.hex()
