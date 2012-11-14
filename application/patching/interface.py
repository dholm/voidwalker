# (void)walker code patching interface
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

from framework.interface.command import PrefixCommand
from framework.interface.command import StackCommand
from framework.interface.command import SupportCommand
from framework.interface.command import register_command
from framework.patching.snippet import SnippetManager
from framework.platform.cpu import Architecture
from framework.target.inferior import InferiorManager
from framework.ui.widgets import Section
from framework.ui.widgets import Table

from ..commands.voidwalker import VoidwalkerCommand


@register_command
class PatchCommand(PrefixCommand):
    '''Commands for patching code'''

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'patch')

    def __init__(self):
        super(PatchCommand, self).__init__()


@register_command
class SnippetCommand(PrefixCommand):
    '''Predefined snippets for patching'''

    @staticmethod
    def name():
        return '%s %s' % (PatchCommand.name(), 'snippet')

    def __init__(self):
        super(SnippetCommand, self).__init__()


@register_command
class ListSnippetsCommand(SupportCommand):
    '''List all the available snippets'''

    @staticmethod
    def name():
        return '%s %s' % (SnippetCommand.name(), 'list')

    def __init__(self):
        super(ListSnippetsCommand, self).__init__()

    def invoke(self, arguments, from_tty):
        table = Table()
        for name, snippet in SnippetManager().snippets():
            row = Table.Row()
            row.add_cell(Table.Cell('%s%s' % ('%(face-identifier)s', name)))
            row.add_cell(Table.Cell('%s%s' % ('%(face-comment)s',
                                              snippet.description())))
            table.add_row(row)

        section = Section('snippets')
        section.add_component(table)
        section.draw(self._terminal, self._terminal.width())


@register_command
class ApplySnippetCommand(StackCommand):
    '''Apply a snippet: <name> <address>

Apply the specified snippet at the specified address. This operation will
overwrite whatever is at that location in memory. The original binary is never
touched by this command.'''

    @staticmethod
    def name():
        return '%s %s' % (SnippetCommand.name(), 'apply')

    def __init__(self):
        super(ApplySnippetCommand, self).__init__()

    def invoke(self, thread, arguments, from_tty):
        if len(arguments) < 2:
            self._terminal.write('%(face-error)sWrong number of arguments!\n')
            return

        inferior = InferiorManager().inferior(thread.inferior_id())
        snippet = SnippetManager().snippet(arguments[0])
        if snippet is None:
            self._terminal.write(' '.join(['%(face-error)sSnippet',
                                           arguments[0],
                                           '%s does not exist!\n']))
            return

        architecture = inferior.cpu().architecture()
        implementation = None
        if ((architecture == Architecture.X86_64 and
             architecture not in snippet.architectures())):
            assert Architecture.X86 in snippet.architectures()
            implementation = snippet.implementation(Architecture.X86)

        else:
            implementation = snippet.implementation(architecture)

        address = abs(long(arguments[1]))
        code = implementation.assemble()
        inferior.write_memory(code, address)
        self._terminal.write('Applied snippet %s%s%s at %s0x%x\n' %
                             ('%(face-identifier)s', arguments[0],
                              '%(face-normal)s', '%(face-constant)s', address))