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


class EflagsRegister(Register):
    _flags = OrderedDict([('c', (1 << 0)), ('p', (1 << 2)), ('a', (1 << 4)),
                          ('z', (1 << 6)), ('s', (1 << 7)), ('t', (1 << 8)),
                          ('i', (1 << 9)), ('d', (1 << 10)), ('o', (1 << 11)),

                          ('nt', (1 << 14)), ('r', (1 << 16)),
                          ('vm', (1 << 17)), ('ac', (1 << 18)),
                          ('vi', (1 << 19)), ('vip', (1 << 20)),
                          ('id', (1 << 21))])

    def __init__(self, name):
        super(EflagsRegister, self).__init__(name)

    def size(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def str(self):
        value = self.value()
        flag_list = []
        for flag, mask in self._flags.iteritems():
            if value & mask:
                flag_list.append('%s ' % flag.upper())

        return ''.join(flag_list)


@register_cpu
class X86Cpu(Cpu):
    _registers = OrderedDict([('gp', ('eax ecx edx ebx esp ebp esi '
                                      'edi').split()),
                              ('fp', ('st0 st1 st2 st3 st4 st5 st6 '
                                      'st7').split()),
                              ('sp', ('cs ss ds es fs gs eip').split())])

    def __init__(self, cpu_factory):
        registers = OrderedDict()
        for group, register_list in self._registers.iteritems():
            registers[group] = [Register(x) for x in register_list]
        registers['sp'].append(EflagsRegister('eflags'))
        super(X86Cpu, self).__init__(cpu_factory, registers)

    @classmethod
    def architecture(cls):
        return Architecture.X86

    def stack_pointer(self):
        return self.register('esp')

    def program_counter(self):
        return self.register('eip')
