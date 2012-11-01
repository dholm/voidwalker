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

from ..command import Command
from ..command import register_command


@register_command
class VoidwalkerCommand(Command):
    _inferior_manager = None
    _terminal = None

    @staticmethod
    def name():
        return 'voidwalker'

    def init(self, terminal):
        self._terminal = terminal

    def __init__(self):
        super(VoidwalkerCommand, self).__init__()

    def invoke(self, argument, from_tty):
        pass
