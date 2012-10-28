# (void)walker base library
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

from arch.architecture import Architecture
from arch.architecture import ArchitectureFactory
from base.decorators import singleton


class Inferior(object):
    _gdb_inferior = None
    _cpu = None

    def __init__(self, inferior_data):
        assert inferior_data['gdb']
        self._gdb_inferior = inferior_data['gdb']
        self._cpu = inferior_data['cpu']

    def num(self):
        return self._gdb_inferior.num

    def cpu(self):
        return self._cpu


@singleton
class InferiorManager(object):
    _file_expression = re.compile((r'`(?P<path>[^\']+)\', '
                                   r'file type (?P<target>\S+).'))
    _inferior_expression = re.compile((r'(?P<num>\d+)\s+'
                                       r'(?P<description>\S+ \S*)\s+'
                                       r'(?P<path>.+)$'))

    _inferiors = {}

    def _target_to_architecture(self, target):
        if re.match(r'.*-x86-64', target):
            return Architecture.X86_64
        if re.match(r'.*-i386', target):
            return Architecture.X86
        if re.match(r'.*-.*mips[^-]*', target):
            return Architecture.MIPS
        if re.match(r'.*-arm[^-]*', target):
            return Architecture.ARM
        return None

    def __init__(self):
        self.autodetect()

    def get_inferior(self, inferior_num):
        if inferior_num in self._inferiors:
            return self._inferiors[inferior_num]
        return None

    def autodetect(self):
        self._inferiors = {}

        targets = {}
        info_target = gdb.execute('info target', False, True)
        if info_target:
            files = self._file_expression.findall(info_target)
            for element in files:
                path = os.path.abspath(element[0]).strip()
                targets[path] = element[1]

        inferiors = {}
        info_inferiors = gdb.execute('info inferiors', False, True)
        if info_inferiors:
            infs = self._inferior_expression.findall(info_inferiors)
            for inferior in infs:
                num = int(inferior[0])
                path = os.path.abspath(inferior[2]).strip()
                assert path in targets
                inferiors[num] = targets[path]

        for inferior in gdb.inferiors():
            assert inferior.num in inferiors
            target = inferiors[inferior.num]
            architecture = self._target_to_architecture(target)
            cpu = ArchitectureFactory().create_cpu(architecture)

            self._inferiors[inferior.num] = Inferior({'gdb': inferior,
                                                      'cpu': cpu})
