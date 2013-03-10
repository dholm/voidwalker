# (void)walker configuration interface
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


class ConfigurationNode(object):
    def __init__(self, parameter=None):
        self._children = {}
        self._parameter = parameter

    def __contains__(self, name):
        return name in self._children

    def __repr__(self):
        s = []
        if self._parameter is not None:
            s += [self._parameter.name(), ': ']
        s.append('{')
        for child in self._children.values():
            s += [repr(child), ', ']
        s.append('}')
        return ''.join(s)

    def append(self, parameter):
        assert parameter.name() not in self._children
        node = ConfigurationNode(parameter)
        name = parameter.name().split(' ')[-1]
        self._children[name] = node

    def value(self):
        return self._parameter.get_value()

    def get(self, name):
        assert name in self._children
        return self._children[name]


class Configuration(object):
    def __init__(self):
        self._root = ConfigurationNode()

    def _get_parent(self, path):
        node = self._root
        for tag in path.split(' ')[:-1]:
            node = node.get(tag)
        return node

    def register_parameter(self, parameter):
        parent = self._get_parent(parameter.name())
        parent.append(parameter)

    def parameter(self, path):
        node = self._root
        for tag in path.split(' '):
            if tag not in node:
                raise KeyError('Parameter %s not found!' % path)
            node = node.get(tag)
        return node

    def __repr__(self):
        return repr(self._root)

