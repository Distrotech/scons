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
import sys
import TestSCons
import TestCmd

python = TestSCons.python

test = TestSCons.TestSCons(match=TestCmd.match_re)

test.subdir('sub1', 'sub2')

test.write('build.py', r"""
import sys
open(sys.argv[1], 'wb').write(open(sys.argv[2], 'rb').read())
sys.exit(0)
""")

test.write('SConstruct', """
B = Builder(action = r"%s build.py $TARGET $SOURCES")
env = Environment()
env['BUILDERS']['B'] = B
env.B(target = 'f1.out', source = 'f1.in')
env.B(target = 'f2.out', source = 'f2.in')
env.B(target = 'f3.out', source = 'f3.in')
SConscript('sub1/SConscript', "env")
SConscript('sub2/SConscript', "env")

foo = Alias('foo')
foo2 = env.Alias('foo', ['f2.out', 'sub1'])
assert foo == foo2
bar = Alias('bar', ['sub2', 'f3.out'])
env.Alias('blat', ['sub2', 'f3.out'])
env.Alias('blat', ['f2.out', 'sub1'])
env.Depends('f1.out', 'bar')

assert Alias('foo') == foo
assert Alias('bar') == bar

""" % python)

test.write(['sub1', 'SConscript'], """
Import("env")
env.B(target = 'f4.out', source = 'f4.in')
env.B(target = 'f5.out', source = 'f5.in')
env.B(target = 'f6.out', source = 'f6.in')
""")

test.write(['sub2', 'SConscript'], """
Import("env")
env.B(target = 'f7.out', source = 'f7.in')
env.B(target = 'f8.out', source = 'f8.in')
env.B(target = 'f9.out', source = 'f9.in')
""")

test.write('f1.in', "f1.in\n")
test.write('f2.in', "f2.in\n")
test.write('f3.in', "f3.in\n")

test.write(['sub1', 'f4.in'], "sub1/f4.in\n")
test.write(['sub1', 'f5.in'], "sub1/f5.in\n")
test.write(['sub1', 'f6.in'], "sub1/f6.in\n")

test.write(['sub2', 'f7.in'], "sub2/f7.in\n")
test.write(['sub2', 'f8.in'], "sub2/f8.in\n")
test.write(['sub2', 'f9.in'], "sub2/f9.in\n")

test.run(arguments = 'foo')

test.fail_test(os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f2.out')))
test.fail_test(os.path.exists(test.workpath('f3.out')))

test.fail_test(not os.path.exists(test.workpath('sub1', 'f4.out')))
test.fail_test(not os.path.exists(test.workpath('sub1', 'f5.out')))
test.fail_test(not os.path.exists(test.workpath('sub1', 'f6.out')))

test.fail_test(os.path.exists(test.workpath('sub2', 'f7.out')))
test.fail_test(os.path.exists(test.workpath('sub2', 'f8.out')))
test.fail_test(os.path.exists(test.workpath('sub2', 'f9.out')))

test.up_to_date(arguments = 'foo')

test.run(arguments = 'f1.out')

test.fail_test(not os.path.exists(test.workpath('f1.out')))
test.fail_test(not os.path.exists(test.workpath('f3.out')))

test.fail_test(not os.path.exists(test.workpath('sub2', 'f7.out')))
test.fail_test(not os.path.exists(test.workpath('sub2', 'f8.out')))
test.fail_test(not os.path.exists(test.workpath('sub2', 'f9.out')))

test.up_to_date(arguments = 'f1.out')

os.unlink(test.workpath('f2.out'))
os.unlink(test.workpath('f3.out'))

test.run(arguments = 'blat')

test.fail_test(not os.path.exists(test.workpath('f2.out')))
test.fail_test(not os.path.exists(test.workpath('f3.out')))

test.write('f3.in', "f3.in 2 \n")

test.run(arguments = 'f1.out',
         stdout = test.wrap_stdout(".* build.py f3.out f3.in\n.* build.py f1.out f1.in\n"))

test.up_to_date(arguments = 'f1.out')

test.write('SConstruct', """
TargetSignatures('content')
B = Builder(action = r"%s build.py $TARGET $SOURCES")
env = Environment()
env['BUILDERS']['B'] = B
env.B(target = 'f1.out', source = 'f1.in')
env.B(target = 'f2.out', source = 'f2.in')
env.B(target = 'f3.out', source = 'f3.in')
SConscript('sub1/SConscript', "env")
SConscript('sub2/SConscript', "env")
env.Alias('foo', ['f2.out', 'sub1'])
env.Alias('bar', ['sub2', 'f3.out'])
env.Alias('blat', ['sub2', 'f3.out'])
env.Alias('blat', ['f2.out', 'sub1'])
env.Depends('f1.out', 'bar')
""" % python)

os.unlink(test.workpath('f1.out'))

test.run(arguments = 'f1.out')

test.fail_test(not os.path.exists(test.workpath('f1.out')))

test.write('f3.in', "f3.in 3 \n")

test.run(arguments = 'f1.out',
         match = TestCmd.match_exact,
         stdout = test.wrap_stdout("""\
%s build.py f3.out f3.in
%s build.py f1.out f1.in
""" % (python, python)))

test.up_to_date(arguments = 'f1.out')

test.pass_test()