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


class CauseRegister(Register):
    '''MIPS Cause Register

    BD - Branch delay slot
    CE - Coprocessor unit
    IP - Interrupt pending

    Exception codes
    Int   - Interrupt
    Mod   - TLB modification
    TLBL  - TLB exception load/instruction fetch
    TLBS  - TLB exception store
    AdEL  - Address error load/instruction fetch
    AdES  - Address error store
    IBE   - Bus error instruction fetch
    DBE   - Bus error data reference: load or store
    Sys   - Syscall
    Bp    - Breakpoint
    RI    - Reserved instruction
    CpU   - Coprocessor unusable
    Ov    - Arithmetic overflow
    Tr    - Trap
    VCEI  - Virtual coherency exception instruction
    FPE   - Floating-point
    WATCH - Reference to WatchHi/WatchLo address
    VCED  - Virtual coherency exception data'''

    _exception = {0: 'Int', 1: 'Mod', 2: 'TLBL', 3: 'TLBS', 4: 'AdEL',
                  5: 'AdES', 6: 'IBE', 7: 'DBE', 8: 'Sys', 9: 'Bp',
                  10: 'RI', 11: 'CpU', 12: 'Ov', 13: 'Tr', 14: 'VCEI',
                  15: 'FPE', 23: 'WATCH', 31: 'VCED'}

    def __init__(self, name):
        super(CauseRegister, self).__init__(name)

    def size(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def str(self):
        value = self.value()
        cause_list = []
        cause_list.append(self._exception.get((value >> 2) & 0x1f, ''))
        for i in range(8, 15):
            if value & (1 << i):
                cause_list.append('IP%d' % i)

        if value & (1 << 11):
            cause_list.append('CE%d' % ((value >> 27) & 3))

        if value & (1 << 31):
            cause_list.append('BD')

        return ' '.join(cause_list)


class StatusRegister(Register):
    '''MIPS Status Register

    CUx - Coprocessor usability
    RP  - Reduced-power operation
    FR  - Additional floating point registers
    RE  - Reverse-endian
    IMx - Interrupt mask
    KX  - 64-bit addressing in kernel mode
    SX  - 64-bit addressing and operations in supervisor mode
    UX  - 64-bit addressing and operations in user mode
    ERL - Error level
    EXL - Exception level
    IE  - Interrupt enable

    Diagnostic Status
    BEV - Location of TLB refill and general exception vectors
    TS  - TLB shutdown
    SR  - Soft reset
    CH  - Cache hit
    CE  - ECC register modified on cache hit
    DE  - Disable ECC exceptions'''

    _flags = {'RP': (1 << 27), 'FR': (1 << 26), 'RE': (1 << 25),
              'KX': (1 << 7), 'SX': (1 << 6), 'UX': (1 << 5), 'EXL': (1 << 1),
              'IE': (1 << 0)}
    _ds_flags = {'BEV': (1 << 22), 'TS': (1 << 21), 'SR': (1 << 20),
                 'CH': (1 << 18), 'CE': (1 << 17), 'DE': (1 << 16)}
    _mode = {2: 'Usr', 1: 'Svi', 0: 'Krn'}

    def __init__(self, name):
        super(StatusRegister, self).__init__(name)

    def size(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def str(self):
        value = self.value()
        status_list = []
        for flag, mask in self._flags.iteritems():
            if value & mask:
                status_list.append('%s' % flag)

        ds_list = []
        for flag, mask in self._ds_flags.iteritems():
            if value & mask:
                ds_list.append('%s' % flag)
        if len(ds_list):
            status_list.append('DS[%s]' % ' '.join(ds_list))

        status_list.append('CU')
        for i in range(28, 31):
            if value & (1 << i):
                status_list.append('%d' % i)

        status_list.append('IM[%02X]' % ((value >> 8) & 0xff))
        status_list.append(self._mode[(value >> 3) & 3])

        return ' '.join(status_list)


@register_cpu
class MipsCpu(Cpu):
    _registers = OrderedDict([('gp', ('zero at v0 v1 a0 a1 a2 a3 t0 t1 t2 t3 '
                                      't4 t5 t6 t7 s0 s1 s2 s3 s4 s5 s6 s7 '
                                      't8 t9 kt0 kt1 gp sp s9 ra').split()),
                              ('sp', ('lo hi bad pc').split())])

    def __init__(self, cpu_factory):
        registers = OrderedDict()
        for group, register_list in self._registers.iteritems():
            registers[group] = [Register(x) for x in register_list]
        registers['sp'].append(CauseRegister('cause'))
        registers['sp'].append(StatusRegister('sr'))
        super(MipsCpu, self).__init__(cpu_factory, registers)

    @classmethod
    def architecture(cls):
        return Architecture.Mips

    def stack_pointer(self):
        return self.register('sp')

    def program_counter(self):
        return self.register('pc')
