# (void)walker CPU architecture support
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

from collections import OrderedDict

from ...framework.platform import Architecture
from ...framework.platform import Cpu
from ...framework.platform import Register
from ...framework.platform import register_cpu

from .x86 import EflagsRegister


@register_cpu
class X8664Cpu(Cpu):
    _registers = OrderedDict([('gp', ('rax rcx rdx rbx rsp rbp rsi rdi r8 r9 '
                                      'r10 r11 r12 r13 r14 r15').split()),
                              ('fp', ('st0 st1 st2 st3 st4 st5 st6 '
                                      'st7').split()),
                              ('sp', ('cs ss ds es fs gs rip').split())])

    def __init__(self, cpu_factory):
        registers = OrderedDict()
        for group, register_list in self._registers.iteritems():
            registers[group] = [Register(x) for x in register_list]
        registers['sp'].append(EflagsRegister('eflags'))
        super(X8664Cpu, self).__init__(cpu_factory, registers)

    @classmethod
    def architecture(cls):
        return Architecture.X8664

    def stack_pointer(self):
        return self.register('rsp')

    def program_counter(self):
        return self.register('rip')
