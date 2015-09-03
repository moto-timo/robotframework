#  Copyright 2008-2015 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .platform import JYTHON
import platform

if JYTHON:

    from org.python.core import PyReflectedFunction, PyReflectedConstructor

    def is_java_init(init):
        return isinstance(init, PyReflectedConstructor)

    def is_java_method(method):
        func = method.im_func if hasattr(method, 'im_func') else method
        return isinstance(func, PyReflectedFunction)

    def is_dotnet_init(init):
        return False

    def is_dotnet_method(method):
        return False

elif platform.python_implementation() == 'IronPython':
    import clr
    clr.AddReference("Microsoft.Dynamic")
    clr.AddReference("Microsoft.Scripting")
    clr.AddReference("IronPython")
    import System
    from System import Type
    from IronPython.Runtime import NameType, PythonContext, PythonFunction
    from IronPython.Runtime.Types import PythonType, ConstructorFunction, BuiltinFunction, BuiltinMethodDescriptor

    def is_dotnet_init(init):
        return isinstance(init, ConstructorFunction)

    def is_dotnet_method(method):
        '''A class method which has been instantiated will be of type IronPython.Runtime.Types.BuiltinMethodDescriptor'''
        func = method.name if hasattr(method, 'Targets') or method.Targets else method
        if hasattr(method, 'Targets'):
            return True
        elif isinstance(func, BuiltinMethodDescriptor):
            return True
        elif isinstance(func, BuiltinFunction):
            return False # class has not been instantiated
        else:
            return False
        #return isinstance(func, BuiltinMethodDescriptor)

    def is_java_init(init):
        return False

    def is_java_method(method):
        return False
else:

    def is_java_init(init):
        return False

    def is_java_method(method):
        return False

    def is_dotnet_init(init):
        return False

    def is_dotnet_method(method):
        return False
