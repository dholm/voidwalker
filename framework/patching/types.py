# (void)walker assembler types
# Copyright (C) 2012 David Holm <dholmster@gmail.com>
#
# Based on Pyasm by Florian Boesch, https://bitbucket.org/pyalot/pyasm/

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

import struct


class ByteStream(object):
    def __init__(self):
        self._buffer = bytes()

    def buffer(self):
        return self._buffer

    def byte(self, value):
        self._buffer += struct.pack('B', value)

    def halfword(self, value):
        self._buffer += struct.pack('H', value)

    def word(self, value):
        self._buffer += struct.pack('I', value)

    def doubleword(self, value):
        self._buffer += struct.pack('Q', value)


class Instruction(object):
    def __init__(self, function, *args, **kwargs):
        self._function = function
        self._name = function.__name__
        self._args = args
        self._kwargs = kwargs

    def __str__(self):
        return '%s %s' % (self._name, ', '.join([str(x) for x in self._args]))

    def assemble(self, stream):
        self._function(stream, *self._args, **self._kwargs)
        return stream

    @classmethod
    def factory(cls, function):
        def builder(*args, **kwargs):
            instruction = cls(function, *args, **kwargs)
            return instruction
        return builder
