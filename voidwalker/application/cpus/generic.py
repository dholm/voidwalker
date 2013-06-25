# (void)walker CPU architecture support
# Copyright (C) 2013 David Holm <dholmster@gmail.com>

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

from ...framework.platform import Architecture
from ...framework.platform import Cpu
from ...framework.platform import Register
from ...framework.platform import register_cpu


@register_cpu
class GenericCpu(Cpu):
    def __init__(self, cpu_factory, registers):
        for group, register_list in registers.iteritems():
            registers[group] = [Register(x) for x in register_list]
        super(GenericCpu, self).__init__(cpu_factory, registers)

    @classmethod
    def architecture(cls):
        return Architecture.Generic

    def stack_pointer(self):
        return self.register('sp')

    def program_counter(self):
        return self.register('pc')
