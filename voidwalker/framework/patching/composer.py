# (void)walker assembler composer
# Based on Pyasm by Florian Boesch, https://bitbucket.org/pyalot/pyasm/
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

from .types import ByteStream


class CodeBlock(object):
    def __init__(self, *instructions):
        self._instructions = list(instructions)

    def __len__(self):
        return len(self._instructions)

    def hex(self):
        stream = ByteStream()
        (x.assemble(stream) for x in self._instructions).next()
        return ' '.join('%02x' % ord(x)
                        for x in stream.buffer())

    def assemble(self):
        stream = ByteStream()
        (x.assemble(stream) for x in self._instructions).next()
        return stream.buffer()
