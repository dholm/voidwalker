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

from collections import OrderedDict

from ..types.instructions import InstructionListing


class Context(object):
    def __init__(self, program_counter):
        self._registers = OrderedDict()
        self._stack = None
        self._instruction_listing = InstructionListing()

        self._program_counter = program_counter

    def stack(self):
        return self._stack

    def register(self, name):
        for register_dict in self._registers.itervalues():
            if name in register_dict:
                return register_dict[name]

        return None

    def registers(self):
        return self._registers.iteritems()

    def instruction_listing(self):
        return self._instruction_listing

    def program_counter(self):
        return self.register(self._program_counter)
