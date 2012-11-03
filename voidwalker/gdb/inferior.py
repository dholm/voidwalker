# (void)walker GDB backend
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
import os.path
import re

from ..platform.architecture import ArchitectureManager
from ..platform.cpu import Architecture
from ..target.inferior import Inferior
from ..target.inferior import InferiorFactory
from ..utils.decorators import singleton_implementation


class GdbInferior(Inferior):
    def __init__(self, cpu, gdb_inferior):
        super(GdbInferior, self).__init__(cpu)
        self._gdb_inferior = gdb_inferior


@singleton_implementation(InferiorFactory)
class GdbInferiorFactory(object):
    _file_expression = re.compile((r'`(?P<path>[^\']+)\', '
                                   r'file type (?P<target>\S+).'))
    _inferior_expression = re.compile((r'(?P<num>\d+)\s+'
                                       r'(?P<description>\S+ \S*)\s+'
                                       r'(?P<path>.+)$'))

    def __init__(self):
        pass

    @staticmethod
    def _target_to_architecture(target):
        if re.match(r'.*-x86-64', target):
            return Architecture.X86_64
        if re.match(r'.*-i386', target):
            return Architecture.X86
        if re.match(r'.*-.*mips[^-]*', target):
            return Architecture.MIPS
        if re.match(r'.*-arm[^-]*', target):
            return Architecture.ARM
        return None

    def create_inferior(self, num):
        gdb_inferior = None
        try:
            gdb_inferior = (i for i in gdb.inferiors() if i.num == num).next()
        except StopIteration:
            pass

        cpu = None
        info_inferiors = gdb.execute('info inferiors', False, True)
        info_target = gdb.execute('info target', False, True)
        try:
            matches = self._inferior_expression.findall(info_inferiors)
            inferior = (i for i in matches if int(i[0]) == num).next()

            inferior_path = os.path.abspath(inferior[2]).strip()
            matches = self._file_expression.findall(info_target)
            target = (i[1] for i in matches
                      if os.path.abspath(i[0]).strip() == inferior_path).next()

            architecture = self._target_to_architecture(target)
            cpu = ArchitectureManager().create_cpu(architecture)

        except TypeError:
            pass

        return GdbInferior(cpu, gdb_inferior)
