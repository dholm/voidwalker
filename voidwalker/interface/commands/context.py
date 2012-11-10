# (void)walker command interface
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

from ...platform.factory import PlatformFactory
from ...target.inferior import InferiorManager
from ...types.data import DataWidget
from ...types.instructions import InstructionListingWidget
from ...ui.widgets import Section
from ...ui.widgets import Table
from ...ui.widgets import Widget
from ..command import DataCommand
from ..command import register_command
from .voidwalker import VoidwalkerCommand


class ContextWidget(Widget):
    def __init__(self, previous_context, context):
        super(ContextWidget, self).__init__()
        self._previous_context = previous_context
        self._context = context

    def _create_registers_section(self, previous_context, context):
        registers_section = Section('registers')
        for group, register_dict in context.registers():
            reg_size = 0
            for name in register_dict.iterkeys():
                reg_size = max(reg_size, len(name))

            table = Table()
            for name, register in register_dict.iteritems():
                contents = [('%(face-identifier)s' +
                             (('%%-%ds: ' % reg_size) % name))]

                value = register.value()
                face = '%(face-constant)s'
                if previous_context.register(register.name()).value() != value:
                    face = '%(face-special)s'

                if value is not None:
                    contents += [('%s%s' % (face, register.str()))]

                else:
                    contents += [('%(face-comment)s' +
                                  (' %(register)s ' %
                                   {'register': register.str()}))]

                cell = Table.Cell(''.join(contents))
                table.add_cell(cell)

            section = Section(group)
            section.add_component(table)
            registers_section.add_component(section)

        return registers_section

    def _create_stack_section(self, context):
        section = Section('stack')
        section.add_component(DataWidget(context.stack()))
        return section

    def _create_code_section(self, context):
        section = Section('code')
        listing = InstructionListingWidget(context.instruction_listing())
        section.add_component(listing)
        return section

    def draw(self, terminal, width):
        section = Section('context')
        regs = self._create_registers_section(self._previous_context,
                                              self._context)
        section.add_component(regs)

        if self._context.stack() is not None and len(self._context.stack()):
            stack = self._create_stack_section(self._context)
            section.add_component(stack)

        if len(self._context.instruction_listing()):
            instructions = self._create_code_section(self._context)
            section.add_component(instructions)

        section.draw(terminal, width)
        terminal.reset()


@register_command
class ContextCommand(DataCommand):
    '''Show the current context.

If the current thread of the inferior is valid the context will be recorded and
dumped. The contents of the context can be controlled using the (void)walker
parameters'''

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'context')

    def init(self, terminal):
        self._terminal = terminal

    def __init__(self):
        super(ContextCommand, self).__init__()
        self._terminal = None

    def invoke(self, thread, argument, from_tty=False):
        if not thread.is_valid():
            return

        inferior = InferiorManager().inferior(thread.inferior_id())
        context = PlatformFactory().create_context(inferior, thread)
        previous_context = context
        if len(thread.contexts()):
            previous_context = thread.contexts()[-1]

        if not from_tty:
            thread.contexts().append(context)

        context_widget = ContextWidget(previous_context, context)
        context_widget.draw(self._terminal, self._terminal.width())
