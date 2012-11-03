# (void)walker GDB backend
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

import gdb

from ..interface.parameter import Parameter
from ..interface.parameter import ParameterBoolean
from ..interface.parameter import ParameterEnum
from ..interface.parameter import ParameterFactory
from ..utils.decorators import singleton_implementation


@singleton_implementation(ParameterFactory)
class GdbParameterFactory(object):
    def create_parameter(self, parameter_type):
        if issubclass(parameter_type, ParameterEnum):
            class GdbParameterEnum(gdb.Parameter, parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)
                    gdb_name = parameter_type.name().replace(' ', '-')
                    gdb.Parameter.__init__(self,
                                           gdb_name,
                                           gdb.COMMAND_SUPPORT,
                                           gdb.PARAM_ENUM,
                                           parameter_type.sequence(self))
                    self.value = parameter_type.default_value(self)

            return GdbParameterEnum()

        elif issubclass(parameter_type, ParameterBoolean):
            class GdbParameterBoolean(gdb.Parameter, parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)
                    gdb_name = parameter_type.name().replace(' ', '-')
                    gdb.Parameter.__init__(self,
                                           gdb_name,
                                           gdb.COMMAND_SUPPORT,
                                           gdb.PARAM_BOOLEAN)
                    self.value = parameter_type.default_value(self)

            return GdbParameterBoolean()

        elif issubclass(parameter_type, Parameter):
            class GdbParameter(parameter_type):
                def __init__(self):
                    parameter_type.__init__(self)

            return GdbParameter()

        else:
            raise TypeError('Parameter type %s unknown!' %
                            str(type(parameter_type)))
