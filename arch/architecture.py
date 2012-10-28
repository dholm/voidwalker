# (void)walker hardware platform support
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

from arch.x86_64 import CpuX8664
from arch.mips import CpuMips
from base.decorators import singleton


class Architecture:
    X86 = 1
    X86_64 = 2
    MIPS = 3
    ARM = 4


@singleton
class ArchitectureFactory:
    _cpu_map = {Architecture.X86_64: CpuX8664,
                Architecture.MIPS: CpuMips}

    def __init__(self):
        self._collector_factory = None

    def init(self, collector_factory):
        self._collector_factory = collector_factory

    def create_cpu(self, architecture):
        assert architecture in self._cpu_map
        return self._cpu_map.get(architecture, None)(self._collector_factory)
