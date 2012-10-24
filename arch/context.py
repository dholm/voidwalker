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

import gdb

class Context(object):
    _cpu = None
    _register_values = None

    def _update_registers(self):
        for register in self._cpu.registers():
            value = register.value()
            self._register_values[register.name()] = value

    def __init__(self, cpu):
        self._cpu = cpu

        self._register_values = {}
        self._update_registers()

    def registers(self):
        return self._register_values.iteritems()
