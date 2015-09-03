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

import sys

from .argumentmapper import ArgumentMapper
from .argumentparser import (PythonArgumentParser, UserKeywordArgumentParser,
                             DynamicArgumentParser, JavaArgumentParser, DotnetArgumentParser)
from .argumentresolver import ArgumentResolver
from .argumentspec import ArgumentSpec
from .argumentvalidator import ArgumentValidator
from .embedded import EmbeddedArguments
if sys.platform.startswith('java'):
    from .javaargumentcoercer import JavaArgumentCoercer
else:
    JavaArgumentCoercer = lambda *args: None
if sys.platform == 'cli':
    from .dotnetargumentcoercer import DotnetArgumentCoercer
else:
    DotnetArgumentCoercer = lambda *args: None
