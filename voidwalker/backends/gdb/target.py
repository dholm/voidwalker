# (void)walker GDB backend
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from ...framework.platform import Architecture
from ...framework.target.inferior import Inferior
from ...framework.target.inferior import InferiorFactory
from ...framework.target.thread import Thread
from ...framework.target.thread import ThreadFactory
from ...framework.types.instructions import Instruction
from ...framework.types.instructions import InstructionListing


class GdbThread(Thread):
    def __init__(self, inferior, gdb_thread):
        super(GdbThread, self).__init__(inferior)
        self._gdb_thread = gdb_thread

    def name(self):
        return self._gdb_thread.name

    def id(self):
        return self._gdb_thread.num

    def is_valid(self):
        return self._gdb_thread.is_valid()


class GdbInferior(Inferior):
    _instruction_exp = re.compile((r'(?P<meta>\S+)?\s*'
                                   r'(?P<address>0x[0-9a-f]+){1}\s*'
                                   r'(?:<(?P<symbol>.+)>){0,1}:\s*'
                                   r'(?P<mnemonic>\S+){1}\s*'
                                   r'(?P<operands>.+)?$'),
                                  re.IGNORECASE)

    def __init__(self, cpu, gdb_inferior):
        super(GdbInferior, self).__init__(cpu)
        self._gdb_inferior = gdb_inferior

    def id(self):
        return self._gdb_inferior.num

    def gdb_inferior(self):
        return self._gdb_inferior

    def disassemble(self, address, length):
        result = gdb.execute(('x /%di 0x%x' % (length + 1, address)),
                             to_string=True)
        parsed = []
        for line in result.split('\n'):
            line = line.replace('%', '%%')
            instruction = self._instruction_exp.search(line)
            if instruction:
                parsed.append(instruction.groupdict())

        listing = InstructionListing()
        for i in range(len(parsed) - 1):
            size = (long(parsed[i + 1]['address'], 16) -
                    long(parsed[i]['address'], 16))
            address = long(parsed[i]['address'], 16)
            data = self.read_memory(address, size)

            symbol = parsed[i]['symbol']
            mnemonic = parsed[i]['mnemonic']
            operands = parsed[i]['operands']
            instruction = Instruction(data, mnemonic, operands, symbol)
            listing.add_instruction(address, instruction)

        return listing

    def read_memory(self, address, length):
        return self._gdb_inferior.read_memory(address, length)

    def write_memory(self, buf, address):
        self._gdb_inferior.write_memory(address, buf)


class GdbInferiorFactory(InferiorFactory, object):
    _file_expression = re.compile((r'`(?P<path>[^\']+)\', '
                                   r'file type (?P<target>\S+).'))
    _inferior_expression = re.compile((r'(?P<num>\d+)\s+'
                                       r'(?P<description>\S+ \S*)\s+'
                                       r'(?P<path>.+)$'))

    def __init__(self, cpu_factory):
        super(GdbInferiorFactory, self).__init__(cpu_factory)

    @classmethod
    def _target_to_architecture(cls, target):
        if re.match(r'.*-x86-64', target):
            return Architecture.X8664
        if re.match(r'.*-i386', target):
            return Architecture.X86
        if re.match(r'.*-.*mips[^-]*', target):
            return Architecture.Mips
        if re.match(r'.*-arm[^-]*', target):
            return Architecture.Arm
        return None

    def create_inferior(self, inferior_id):
        gdb_inferior = None
        try:
            gdb_inferior = (i for i in gdb.inferiors()
                            if i.num == inferior_id).next()
        except StopIteration:
            return None

        cpu = None
        info_inferiors = gdb.execute('info inferiors', False, True)
        info_target = gdb.execute('info target', False, True)
        try:
            matches = self._inferior_expression.findall(info_inferiors)
            inferior = (i for i in matches if int(i[0]) == inferior_id).next()

            inferior_path = os.path.abspath(inferior[2]).strip()
            matches = self._file_expression.findall(info_target)
            target = (i[1] for i in matches
                      if os.path.abspath(i[0]).strip() == inferior_path).next()

            architecture = self._target_to_architecture(target)
            cpu = self._cpu_factory.create_cpu(architecture)

        except TypeError:
            return None

        return GdbInferior(cpu, gdb_inferior)


class GdbThreadFactory(ThreadFactory, object):
    def create_thread(self, inferior, thread_id):
        gdb_thread = None
        try:
            gdb_thread = (i for i in inferior.gdb_inferior().threads()
                          if i.num == thread_id).next()
            thread = GdbThread(inferior, gdb_thread)
            inferior.add_thread(thread)
            return thread

        except StopIteration:
            pass

        return None
