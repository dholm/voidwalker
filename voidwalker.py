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

# Register all commands, parameters, cpus and themes
from voidwalker.gdb import *
from voidwalker.interface.commands import *
from voidwalker.interface.parameters import *
from voidwalker.platform.cpus import *
from voidwalker.ui.themes import *

from voidwalker.gdb.convenience import ConvenienceManager
from voidwalker.gdb.terminal import GdbTerminal
from voidwalker.interface.command import CommandManager
from voidwalker.interface.parameter import ParameterManager
from voidwalker.target.inferior import InferiorManager
from voidwalker.ui.theme import ThemeManager


version = '0.0.0'

ParameterManager().init()
terminal = GdbTerminal()
ThemeManager().init(terminal.depth())
CommandManager().init(terminal)
InferiorManager().init()
ConvenienceManager().init()

terminal.write(('%(face-underlined)s(void)walker%(face-normal)s '
                'v%(version)s installed%(face-reset)s\n'),
               {'version': version})
