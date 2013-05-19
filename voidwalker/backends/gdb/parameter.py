# (void)walker GDB backend
# Copyright (C) 2012-2013 David Holm <dholmster@gmail.com>

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

from ...framework.interface.parameter import BooleanParameter
from ...framework.interface.parameter import EnumParameter
from ...framework.interface.parameter import IntegerParameter
from ...framework.interface.parameter import Parameter
from ...framework.interface.parameter import PrefixParameter


class GdbBaseParameter(gdb.Parameter, object):
    def __init__(self, name, command, param, sequence=None):
        if param == gdb.PARAM_ENUM:
            gdb.Parameter.__init__(self, name, command, param, sequence)
        else:
            gdb.Parameter.__init__(self, name, command, param)

    def get_value(self):
        return self.value

    def get_set_string(self):
        return str(self.value)

    def get_show_string(self, value):
        return value


class GdbParameterFactory(object):
    def create_enum_parameter(self, parameter_type):
        class GdbParameterEnum(GdbBaseParameter, parameter_type):
            __doc__ = parameter_type.__doc__
            show_doc = __doc__
            set_doc = __doc__

            def __init__(self):
                parameter_type.__init__(self)
                gdb_name = parameter_type.name().replace(' ', '-')
                GdbBaseParameter.__init__(self, gdb_name,
                                          gdb.COMMAND_SUPPORT,
                                          gdb.PARAM_ENUM,
                                          parameter_type.sequence(self))
                self.value = parameter_type.default_value(self)

        return GdbParameterEnum()

    def create_integer_parameter(self, parameter_type):
        class GdbParameterInteger(GdbBaseParameter, parameter_type):
            __doc__ = parameter_type.__doc__
            show_doc = __doc__
            set_doc = __doc__

            def __init__(self):
                parameter_type.__init__(self)
                gdb_name = parameter_type.name().replace(' ', '-')
                GdbBaseParameter.__init__(self, gdb_name,
                                          gdb.COMMAND_SUPPORT,
                                          gdb.PARAM_ZINTEGER)
                self.value = parameter_type.default_value(self)

        return GdbParameterInteger()

    def create_boolean_parameter(self, parameter_type):
        class GdbParameterBoolean(GdbBaseParameter, parameter_type):
            __doc__ = parameter_type.__doc__
            show_doc = __doc__
            set_doc = __doc__

            def __init__(self):
                parameter_type.__init__(self)
                gdb_name = parameter_type.name().replace(' ', '-')
                GdbBaseParameter.__init__(self, gdb_name,
                                          gdb.COMMAND_SUPPORT,
                                          gdb.PARAM_BOOLEAN)
                self.value = parameter_type.default_value(self)

        return GdbParameterBoolean()

    def create_generic_parameter(self, parameter_type):
        class GdbParameter(parameter_type):
            __doc__ = parameter_type.__doc__

            def __init__(self):
                parameter_type.__init__(self)

        return GdbParameter()

    def create(self, parameter_type):
        create_method = [(EnumParameter, self.create_enum_parameter),
                         (IntegerParameter, self.create_integer_parameter),
                         (BooleanParameter, self.create_boolean_parameter),
                         (PrefixParameter, self.create_generic_parameter),
                         (Parameter, self.create_generic_parameter)]
        for ptype, create in create_method:
            if issubclass(parameter_type, ptype):
                return create(parameter_type)

        else:
            raise TypeError('Parameter %s of type %s unknown!' %
                            parameter_type.name(), str(type(parameter_type)))
