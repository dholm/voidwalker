# (void)walker GDB-specific interface
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

from ....framework.interface.command import PrefixCommand
from ....framework.interface.command import register_command

from ....application.commands.voidwalker import VoidwalkerCommand


@register_command
class GdbCommand(PrefixCommand):
    '''Commands for interacting with GDB'''

    @staticmethod
    def name():
        return '%s %s' % (VoidwalkerCommand.name(), 'gdb')

    def __init__(self):
        super(GdbCommand, self).__init__()
