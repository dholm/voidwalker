# (void)walker command line interface
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

import abc

from ..utils.decorators import singleton
from ..utils.decorators import singleton_specification


_parameter_list = []


class Parameter(object):
    def init(self):
        pass

    @staticmethod
    def name():
        raise NotImplementedError

    def default_value(self):
        raise NotImplementedError


class PrefixParameter(Parameter):
    @classmethod
    def get_value(cls):
        raise TypeError

    def default_value(self):
        raise NotImplementedError


class BooleanParameter(Parameter):
    def default_value(self):
        raise NotImplementedError


class EnumParameter(Parameter):
    def sequence(self):
        raise NotImplementedError


class IntegerParameter(Parameter):
    def default_value(self):
        raise NotImplementedError


class ParameterFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create_parameter(self, parameter_type):
        raise NotImplementedError


class ParameterBuilder(object):
    def __init__(self, factory, config):
        for Param in _parameter_list:
            param = factory.create_parameter(Param)
            param.init()
            config.register_parameter(param)


def register_parameter(cls):
    _parameter_list.append(cls)
    return cls
