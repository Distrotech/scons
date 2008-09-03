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

"""
Verify that AddPostAction() on a program target doesn't interfere with
linking.

This is a test for fix of Issue 1004, reported by Matt Doar and
packaged by Gary Oberbrunner.
"""

import string

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()

test.write('strip.py', """\
import string
import sys
print "strip.py: %s" % string.join(sys.argv[1:])
""")

test.write('SConstruct', """\
env = Environment()

mylib = env.StaticLibrary('mytest', 'test_lib.c')

myprog = env.Program('test1.c',
                     LIBPATH = ['.'],
                     LIBS = ['mytest'],
                     OBJSUFFIX = '.obj',
                     PROGSUFFIX = '.exe')
if ARGUMENTS['case']=='2':
  AddPostAction(myprog, Action(r'%(_python_)s strip.py ' + myprog[0].abspath))
""" % locals())

test.write('test1.c', """\
extern void test_lib_fn();
int main(int argc, char **argv) {
  test_lib_fn();
  return 0;
}
""")

test.write('test_lib.c', r"""\
#include <stdio.h>

void test_lib_fn() {
  printf("Hello world\n");
}
""")

test.run(arguments="-Q case=1", stderr=None)

test.run(arguments="-Q -c case=1")

test.must_not_exist('test1.obj')

test.run(arguments="-Q case=2", stderr=None)

expect = 'strip.py: %s' % test.workpath('test1.exe')
test.fail_test(string.find(test.stdout(), expect) == -1)

test.pass_test()