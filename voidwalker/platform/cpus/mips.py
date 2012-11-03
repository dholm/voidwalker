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

from ..cpu import Architecture
from ..cpu import Cpu
from ..architecture import register_cpu


@register_cpu
class MipsCpu(Cpu):
    _register_list = ('v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 t4 t5 t6 t7 t8 t9 s0 s1 '
                      's2 s3 s4 s5 s6 s7 s8 zero at gp sp kt0 kt1').split()

    def __init__(self):
        super(MipsCpu, self).__init__(self._register_list)

    @staticmethod
    def architecture():
        return Architecture.MIPS

    def stack_pointer(self):
        return self.register('sp')
