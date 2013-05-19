# (void)walker nop snippets
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

from ...framework.patching.composer import CodeBlock
from ...framework.patching.snippet import Snippet
from ...framework.patching.snippet import register_snippet
from ...framework.platform.cpu import Architecture

from ..cpus import mips_instructions as mips
from ..cpus import x86_instructions as x86


@register_snippet
class NopSnippet(Snippet):
    _code = {Architecture.X86: CodeBlock(x86.nop()),
             Architecture.Mips: CodeBlock(mips.nop())}

    def __init__(self):
        pass

    def architectures(self):
        return NopSnippet._code.iterkeys()

    def len(self, architecture):
        code = self.implementation(architecture)
        return len(code)

    def implementation(self, architecture):
        assert architecture in NopSnippet._code.iterkeys()
        return NopSnippet._code[architecture]

    @staticmethod
    def description():
        return ('No-operations are used to overwrite instructions that '
                'shouldn\'t be executed')

    @staticmethod
    def name():
        return 'nop'
