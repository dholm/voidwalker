# (void)walker GDB plugin
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

import inspect
import os.path
import sys
voidwalker_path = os.path.abspath(inspect.getfile(inspect.currentframe()))
sys.path.append(os.path.dirname(voidwalker_path))

from arch.architecture import ArchitectureFactory
from interface.context import ContextCommand
from interface.gdb_collector import GdbCollectorFactory
from ui.theme import ThemeManager
import interface
import interface.gdb_command
import interface.gdb_parameter


from ui.gdb_terminal import GdbTerminal

version = '0.0.0'

interface.parameters.ParameterManager().init(interface.gdb_parameter.factory)
ArchitectureFactory().init(GdbCollectorFactory())

terminal = GdbTerminal()
ThemeManager().init(terminal.depth())
terminal.write(('%(face-underlined)s(void)walker%(face-normal)s '
                'v%(version)s installed%(face-reset)s\n'),
               {'version': version})

interface.commands.CommandManager().init(interface.gdb_command.factory,
                                         terminal)
