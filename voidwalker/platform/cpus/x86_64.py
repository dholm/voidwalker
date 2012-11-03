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
class X8664Cpu(Cpu):
    _register_list = ('rax rbx rcx rdx rsi rdi rbp rsp r8 r9 r10 r11 r12 r13 '
                      'r14 r15 rip cs ss ds es fs gs').split()

    def __init__(self):
        super(X8664Cpu, self).__init__(self._register_list)

    @staticmethod
    def architecture():
        return Architecture.X86_64

    def stack_pointer(self):
        return self.register('rsp')
