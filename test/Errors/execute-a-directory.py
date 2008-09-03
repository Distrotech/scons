#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import os
import string

import TestSCons

test = TestSCons.TestSCons()

not_executable = test.workpath("not_executable")

test.write(not_executable, "\n")

test.write("f3.in", "\n")

test.write('SConstruct', r"""
bld = Builder(action = '%s $SOURCES $TARGET')
env = Environment(BUILDERS = { 'bld' : bld })
env.bld(target = 'f3', source = 'f3.in')
""" % string.replace(test.workdir, '\\', '\\\\'))

test.run(arguments='.',
         stdout = test.wrap_stdout("%s f3.in f3\n" % test.workdir, error=1),
         stderr = None,
         status = 2)

bad_command = """\
Bad command or file name
"""

unrecognized = """\
'%s' is not recognized as an internal or external command,
operable program or batch file.
scons: *** [%s] Error 1
"""

unspecified = """\
The name specified is not recognized as an
internal or external command, operable program or batch file.
scons: *** [%s] Error 1
"""

cannot_execute = """\
%s: cannot execute
scons *** [%s] Error 126
"""

Permission_denied = """\
%s: Permission denied
scons: *** [%s] Error 126
"""

permission_denied = """\
%s: permission denied
scons: *** [%s] Error 126
"""

is_a_directory = """\
%s: is a directory
scons: *** [%s] Error 126
"""

test.description_set("Incorrect STDERR:\n%s\n" % test.stderr())
if os.name == 'nt':
    errs = [
        bad_command,
        unrecognized % (test.workdir, 'f3'),
        unspecified % 'f3'
    ]
    test.fail_test(not test.stderr() in errs)
else:
    errs = [
        cannot_execute % (not_executable, 'f3'),
        is_a_directory % (test.workdir, 'f3'),
        Permission_denied % (test.workdir, 'f3'),
        Permission_denied % (test.workdir, 'f3'),
    ]
    error_message_not_found = 1
    for err in errs:
        if string.find(test.stderr(), err) != -1:
            error_message_not_found = None
            break
    test.fail_test(error_message_not_found)

test.pass_test()