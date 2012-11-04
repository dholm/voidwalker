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

import string

from ...platform.factory import PlatformFactory
from ...target.inferior import InferiorManager
from ...types.data import DataWidget
from ...ui.widgets import Section
from ...ui.widgets import Table
from ...ui.widgets import Widget
from ..command import DataCommand
from ..command import register_command
from ..parameters.show import ShowInstructionsParameter
from ..parameters.show import ShowRegistersParameter
from ..parameters.show import ShowStackParameter
from .voidwalker import VoidwalkerCommand


class ContextWidget(Widget):
    _register_fmt = {16: '0x%032lX',
                     8: '0x%016lX',
                     4: '0x%08lX',
                     2: '0x%04lX'}

    def __init__(self, previous_context, context):
        super(ContextWidget, self).__init__()
        self._previous_context = previous_context
        self._context = context

    def _create_registers_section(self, previous_context, context):
        table = Table()
        reg_size = 0
        for name, register in context.registers():
            reg_size = max(reg_size, len(name))

        for name, register in context.registers():
            contents = [('%(face-identifier)s' +
                         (('%%-%ds: ' % reg_size) % name))]

            size = register.size()
            value = register.value()
            face = '%(face-constant)s'
            if previous_context.register(name).value() != value:
                face = '%(face-special)s'

            if value is not None:
                contents += [('%s%s' % (face,
                                        (self._register_fmt[size] % value)))]
            else:
                contents += [('%(face-comment)s' +
                              ' %(dashes)s ' % {'dashes': '-' * size * 2})]

            cell = Table.Cell(''.join(contents))
            table.add_cell(cell)

        section = Section('registers')
        section.add_component(table)
        return section

    def _create_stack_section(self, context):
        section = Section('stack')
        section.add_component(DataWidget(context.stack()))
        return section

    def _create_instructions_section(self, context):
        table = Table()
        for instruction in context.instructions():
            row = Table.Row()

            face = '%(face-normal)s'
            if instruction['meta']:
                face = '%(face-underlined)s'

            row.add_cell(Table.Cell('%s%s' % (face, instruction['address'])))

            if instruction['symbol']:
                row.add_cell(Table.Cell('%(face-identifier)s' +
                                        instruction['symbol']))
            else:
                row.add_cell(Table.Cell())

            row.add_cell(Table.Cell('%s%s' %
                                    (face, instruction['mnemonic'])))

            if instruction['operands']:
                row.add_cell(Table.Cell('%s%s' %
                                        (face, instruction['operands'])))
            else:
                row.add_cell(Table.Cell())

            table.add_row(row)

        section = Section('code')
        section.add_component(table)
        return section

    def draw(self, terminal, width):
        section = Section('context')
        draw_section = False
        if ShowRegistersParameter.get_value():
            regs = self._create_registers_section(self._previous_context,
                                                  self._context)
            section.add_component(regs)
            draw_section = True

        if ShowStackParameter.get_value():
            stack = self._create_stack_section(self._context)
            section.add_component(stack)
            draw_section = True

        if ShowInstructionsParameter.get_value():
            instructions = self._create_instructions_section(self._context)
            section.add_component(instructions)
            draw_section = True

        if draw_section:
            section.draw(terminal, width)
            terminal.reset()


@register_command
class ContextCommand(DataCommand):
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
