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


class Parameter(object):
    __metaclass__ = abc.ABCMeta

    def init(self):
        pass

    @staticmethod
    def name():
        raise NotImplementedError

    @abc.abstractmethod
    def default_value(self):
        raise NotImplementedError


class PrefixParameter(Parameter):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def get_value(cls):
        raise TypeError

    @abc.abstractmethod
    def default_value(self):
        raise NotImplementedError


class BooleanParameter(Parameter):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def default_value(self):
        raise NotImplementedError


class EnumParameter(Parameter):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def sequence(self):
        raise NotImplementedError


class IntegerParameter(Parameter):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def default_value(self):
        raise NotImplementedError


class ParameterFactory(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, parameter_type):
        raise NotImplementedError


class ParameterBuilder(object):
    def __init__(self, factory, config):
        for Param in _parameter_list:
            param = factory.create(Param)
            param.init()
            config.register_parameter(param)


def register_parameter(cls):
    _parameter_list.append(cls)
    return cls

_parameter_list = []
