# (void)walker platform test implementation
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

from collections import OrderedDict

from ...framework.platform import Architecture
from ...framework.platform import Context
from ...framework.platform import Cpu
from ...framework.platform import CpuFactory
from ...framework.platform import PlatformFactory
from ...framework.platform import Register
from ...framework.platform import create_static_register
from ...framework.platform import register_cpu


@register_cpu
class TestCpu(Cpu):
    register_dict = OrderedDict([('gp', ('r0 r1').split()),
                                 ('sp', ('pc sp flags').split())])

    def __init__(self, cpu_factory):
        registers = OrderedDict()
        for group, register_list in self.register_dict.items():
            registers[group] = [Register(x) for x in register_list]
        super(TestCpu, self).__init__(cpu_factory, registers)

    @classmethod
    def architecture(cls):
        return Architecture.Test

    def stack_pointer(self):
        return self.register('sp')

    def program_counter(self):
        return self.register('pc')


class TestCpuFactory(CpuFactory):
    def __init__(self):
        self._registers = None

    def create_cpu(self, architecture):
        return TestCpu(self)

    def create_register(self, cpu, register):
        class TestRegister(type(register), object):
            def __init__(self, name):
                super(TestRegister, self).__init__(name)
                self._size = 8
                self._value = 0

            def size(self):
                return self._size

            def value(self):
                return self._value

        return TestRegister(register.name())


class TestPlatformFactory(PlatformFactory, object):
    def __init__(self):
        self._registers = None
        self.reset()

    def reset(self):
        self._registers = {}

    def create_context(self, config, inferior, thread):
        class TestContext(Context):
            def __init__(self):
                sp = inferior.cpu().stack_pointer()
                super(TestContext, self).__init__(sp)

                for group, register_dict in inferior.cpu().registers():
                    register_dict = dict((x.name(), create_static_register(x))
                                         for x in register_dict.itervalues())
                    self._registers[group] = register_dict

        return TestContext()
