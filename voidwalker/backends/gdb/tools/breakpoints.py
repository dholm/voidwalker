# (void)walker GDB breakpoint control
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

import gdb
import re

from ....framework.interface.command import BreakpointCommand
from ....framework.interface.command import PrefixCommand
from ....framework.interface.command import register_command

from .interface import GdbCommand


@register_command
class BreakCommand(PrefixCommand):
    '''Commands for GDB breakpoints'''

    @staticmethod
    def name():
        return '%s %s' % (GdbCommand.name(), 'break')

    def __init__(self):
        super(BreakCommand, self).__init__()


@register_command
class BreakTextCommand(BreakpointCommand):
    '''Break on text section entry point

Sets a breakpoint at the text section entrypoint. This command is useful if
there are no symbols and no known address to set a breakpoint at.'''

    _text_exp = re.compile(r'(?P<start>0x[0-9a-z]+)\s*-\s*(?P<end>0x[0-9a-z]+)'
                           r'\s+is\s+(?P<section>[^\s]+)', re.IGNORECASE)

    @staticmethod
    def name():
        return '%s %s' % (BreakCommand.name(), 'text')

    def __init__(self):
        super(BreakTextCommand, self).__init__()
        self._terminal = None

    def invoke(self, thread, argument, from_tty=False):
        sections = gdb.execute('info target', to_string=True)
        address = None
        for match in self._text_exp.finditer(sections):
            if match.group('section') == '.text':
                address = abs(long(match.group('start'), 16))
                break

        if address is not None:
            gdb.Breakpoint('*0x%x' % address)
        else:
            raise gdb.error('Unable to locate .text section!')
