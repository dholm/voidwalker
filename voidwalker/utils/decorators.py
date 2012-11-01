# (void)walker utility library
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


def singleton(cls):
    instances = {}

    def instance():
        if cls not in instances:
            instances[cls] = cls()

        return instances[cls]

    return instance


@singleton
class SingletonManager(object):
    def __init__(self):
        self._singletons = {}

    def add_specification(self, cls):
        assert cls not in self._singletons
        self._singletons[cls] = None

    def has_specification(self, spec):
        return spec in self._singletons

    def add_implementation(self, spec, cls):
        if spec not in self._singletons:
            self.add_specification(spec)
        self._singletons[spec] = cls()

    def has_implementation(self, spec):
        if spec in self._singletons:
            return self._singletons[spec] is not None
        return False

    def get_implementation(self, spec):
        return self._singletons[spec]


def singleton_specification(cls):
    def instance():
        if SingletonManager().has_specification(cls):
            return SingletonManager().get_implementation(cls)

        else:
            return cls

    return instance


def singleton_implementation(spec):
    def register(impl):
        SingletonManager().add_implementation(spec(), impl)

    return register
