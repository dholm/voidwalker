# (void)walker code patching interface
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from flowui.widgets import Section
from flowui.widgets.table import Cell
from flowui.widgets.table import Row
from flowui.widgets.table import Table

from ...framework.interface import PrefixCommand
from ...framework.interface import StackCommand
from ...framework.interface import SupportCommand
from ...framework.interface import register_command
from ...framework.platform import Architecture

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


class SnippetCommandBuilder(object):
    def __init__(self, snippet_repository):
        @register_command
        class ListSnippetsCommand(SupportCommand):
            '''List all the available snippets'''

            @staticmethod
            def name():
                return '%s %s' % (SnippetCommand.name(), 'list')

            def __init__(self):
                super(ListSnippetsCommand, self).__init__()

            def execute(self, terminal, *_):
                table = Table()
                for name, snippet in snippet_repository.snippets():
                    row = Row()
                    row.add_cell(Cell('%s%s' % ('%(face-identifier)s', name)))
                    row.add_cell(Cell('%s%s' % ('%(face-comment)s',
                                                snippet.description())))
                    table.add_row(row)

                section = Section('snippets')
                section.add_component(table)
                section.draw(terminal, terminal.width())

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

            def execute(self, config, terminal, thread, platform_factory,
                        argument):
                if len(argument) < 2:
                    terminal.write('%(face-error)s'
                                   'Wrong number of arguments!\n')
                    return

                inferior = thread.get_inferior()
                snippet = snippet_repository.snippet(argument[0])
                if snippet is None:
                    terminal.write(' '.join(['%(face-error)sSnippet',
                                             argument[0],
                                             '%s does not exist!\n']))
                    return

                architecture = inferior.cpu().architecture()
                implementation = None
                if ((architecture == Architecture.X8664 and
                     architecture not in snippet.architectures())):
                    assert Architecture.X86 in snippet.architectures()
                    implementation = snippet.implementation(Architecture.X86)

                else:
                    implementation = snippet.implementation(architecture)

                address = abs(long(argument[1]))
                code = implementation.assemble()
                inferior.write_memory(code, address)

                terminal.write('Applied snippet %s%s%s at %s0x%x\n' %
                               ('%(face-identifier)s', argument[0],
                                '%(face-normal)s', '%(face-constant)s',
                                address))
