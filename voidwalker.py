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
sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

import cmds

from base.inferiors import InferiorManager
from ui.solarized import Solarized
from ui.terminal import GdbTerminal

version = '0.0.0'

terminal = GdbTerminal(Solarized())
terminal.write(('Loading %(face-emphasized)s(void)walker%(face-default)s '
                'v%(version)s%(face-none)s\n'), {'version': version})

cmds.commands.CommandManager().init(InferiorManager, terminal)
