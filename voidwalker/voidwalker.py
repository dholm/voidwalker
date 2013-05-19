# (void)walker GDB plugin
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

from flowui.terminal import AnsiTerminal
from flowui.themes import Solarized

from .framework.interface import CommandBuilder
from .framework.interface import Configuration
from .framework.interface import ParameterBuilder
from .framework.patching import SnippetRepository
from .framework.target import InferiorRepository

from .backends.gdb import GdbCommandFactory
from .backends.gdb import GdbCpuFactory
from .backends.gdb import GdbParameterFactory
from .backends.gdb import GdbPlatformFactory
from .backends.gdb import GdbInferiorFactory
from .backends.gdb import GdbThreadFactory
from .backends.gdb import GdbTerminal

from .application.patching import SnippetCommandBuilder

# Register all commands, parameters, cpus and themes
from .backends.gdb import tools
from . import application

from version import __version__


class VoidwalkerBuilder(object):
    def __init__(self, version):
        config = Configuration()
        ParameterBuilder(GdbParameterFactory(), config)

        snippet_repository = SnippetRepository()
        SnippetCommandBuilder(snippet_repository)

        platform_factory = GdbPlatformFactory()
        inferior_factory = GdbInferiorFactory(GdbCpuFactory())
        inferior_repository = InferiorRepository()
        ansi_terminal = AnsiTerminal(GdbTerminal(), Solarized())
        CommandBuilder(GdbCommandFactory(), inferior_repository,
                       platform_factory, inferior_factory, GdbThreadFactory(),
                       config, ansi_terminal)

        ansi_terminal.write(('%(face-underlined)s(void)walker%(face-normal)s '
                             'v%(version)s installed\n'),
                            {'version': version})


voidwalker_builder = VoidwalkerBuilder(__version__)
