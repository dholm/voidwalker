# (void)walker application interface
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

from base.decorators import singleton


class Parameter(object):
    def init(self):
        raise NotImplementedError

    def default_value(self):
        raise NotImplementedError


class ParameterEnum(Parameter):
    def sequence(self):
        raise NotImplementedError


@singleton
class ParameterManager(object):
    _parameters = {}
    _instances = {}

    def init(self, parameter_factory):
        for name, Param in self._parameters.iteritems():
            self._instances[name] = parameter_factory(Param)
            self._instances[name].init()

    def add_parameter(self, parameter):
        self._parameters[parameter.name()] = parameter

    def get_parameter(self, name):
        assert name in self._instances
        return self._instances[name]


def register_parameter(cls):
    ParameterManager().add_parameter(cls)
    return cls
