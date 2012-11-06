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

from ..interface.parameters.context import ContextInstructionsParameter
from ..interface.parameters.context import ContextStackParameter


class Context(object):
    def __init__(self, instruction_pointer):
        self._registers = OrderedDict()
        self._stack = None
        self._instructions = OrderedDict()

        self._instruction_pointer = instruction_pointer

    def _param_stackdw(self):
        return ContextStackParameter.get_value()

    def _param_instructions(self):
        return ContextInstructionsParameter.get_value()

    def stack(self):
        return self._stack

    def register(self, name):
        for register_dict in self._registers.itervalues():
            if name in register_dict:
                return register_dict[name]

        return None

    def registers(self):
        return self._registers.iteritems()

    def instructions(self):
        if not len(self._instructions):
            return None
        return self._instructions.iteritems()

    def instruction_pointer(self):
        return self.register(self._instruction_pointer)
