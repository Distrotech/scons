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
Test that we can generate Visual Studio 6 project (.dsp) and solution
(.dsw) files that look correct.
"""

import os
import sys

import TestSConsMSVS

test = TestSConsMSVS.TestSConsMSVS()

# Make the test infrastructure think we have this version of MSVS installed.
test._msvs_versions = ['6.0']



expected_dspfile = TestSConsMSVS.expected_dspfile_6_0
expected_dswfile = TestSConsMSVS.expected_dswfile_6_0
SConscript_contents = TestSConsMSVS.SConscript_contents_6_0



test.subdir('work1')

test.write(['work1', 'SConstruct'], SConscript_contents)

test.run(chdir='work1', arguments="Test.dsp")

test.must_exist(test.workpath('work1', 'Test.dsp'))
dsp = test.read(['work1', 'Test.dsp'], 'r')
expect = test.msvs_substitute(expected_dspfile, '6.0', 'work1', 'SConstruct')
# don't compare the pickled data
assert dsp[:len(expect)] == expect, test.diff_substr(expect, dsp)

test.must_exist(test.workpath('work1', 'Test.dsw'))
dsw = test.read(['work1', 'Test.dsw'], 'r')
expect = test.msvs_substitute(expected_dswfile, '6.0', 'work1', 'SConstruct')
assert dsw == expect, test.diff_substr(expect, dsw)

test.run(chdir='work1', arguments='-c .')

test.must_not_exist(test.workpath('work1', 'Test.dsp'))
test.must_not_exist(test.workpath('work1', 'Test.dsw'))

test.run(chdir='work1', arguments='Test.dsp')

test.must_exist(test.workpath('work1', 'Test.dsp'))
test.must_exist(test.workpath('work1', 'Test.dsw'))

test.run(chdir='work1', arguments='-c Test.dsw')

test.must_not_exist(test.workpath('work1', 'Test.dsp'))
test.must_not_exist(test.workpath('work1', 'Test.dsw'))



test.subdir('work2', ['work2', 'src'])

test.write(['work2', 'SConstruct'], """\
SConscript('src/SConscript', variant_dir='build')
""")

test.write(['work2', 'src', 'SConscript'], SConscript_contents)

test.run(chdir='work2', arguments=".")

dsp = test.read(['work2', 'src', 'Test.dsp'], 'r')
expect = test.msvs_substitute(expected_dspfile, '6.0', 'work2', 'SConstruct')
# don't compare the pickled data
assert dsp[:len(expect)] == expect, test.diff_substr(expect, dsp)

test.must_exist(test.workpath('work2', 'src', 'Test.dsw'))
dsw = test.read(['work2', 'src', 'Test.dsw'], 'r')
expect = test.msvs_substitute(expected_dswfile, '6.0',
                              os.path.join('work2', 'src'))
assert dsw == expect, test.diff_substr(expect, dsw)

test.must_match(['work2', 'build', 'Test.dsp'], """\
This is just a placeholder file.
The real project file is here:
%s
""" % test.workpath('work2', 'src', 'Test.dsp'),
                mode='r')

test.must_match(['work2', 'build', 'Test.dsw'], """\
This is just a placeholder file.
The real workspace file is here:
%s
""" % test.workpath('work2', 'src', 'Test.dsw'),
                mode='r')



test.subdir('work3')

test.write(['work3', 'SConstruct'], """\
env=Environment(platform='win32', tools=['msvs'], MSVS_VERSION='6.0')

testsrc = ['test.c']
testincs = ['sdk.h']
testlocalincs = ['test.h']
testresources = ['test.rc']
testmisc = ['readme.txt']

p = env.MSVSProject(target = 'Test.dsp',
                    srcs = testsrc,
                    incs = testincs,
                    localincs = testlocalincs,
                    resources = testresources,
                    misc = testmisc,
                    buildtarget = 'Test.exe',
                    variant = 'Release',
                    auto_build_solution = 0)

env.MSVSSolution(target = 'Test.dsw',
                 slnguid = '{SLNGUID}',
                 projects = [p],
                 variant = 'Release')
""")

test.run(chdir='work3', arguments=".")

test.must_exist(test.workpath('work3', 'Test.dsp'))
dsp = test.read(['work3', 'Test.dsp'], 'r')
expect = test.msvs_substitute(expected_dspfile, '6.0', 'work3', 'SConstruct')
# don't compare the pickled data
assert dsp[:len(expect)] == expect, test.diff_substr(expect, dsp)

test.must_exist(test.workpath('work3', 'Test.dsw'))
dsw = test.read(['work3', 'Test.dsw'], 'r')
expect = test.msvs_substitute(expected_dswfile, '6.0', 'work3', 'SConstruct')
assert dsw == expect, test.diff_substr(expect, dsw)

test.run(chdir='work3', arguments='-c .')

test.must_not_exist(test.workpath('work3', 'Test.dsp'))
test.must_not_exist(test.workpath('work3', 'Test.dsw'))

test.run(chdir='work3', arguments='.')

test.must_exist(test.workpath('work3', 'Test.dsp'))
test.must_exist(test.workpath('work3', 'Test.dsw'))

test.run(chdir='work3', arguments='-c Test.dsw')

test.must_exist(test.workpath('work3', 'Test.dsp'))
test.must_not_exist(test.workpath('work3', 'Test.dsw'))

test.run(chdir='work3', arguments='-c Test.dsp')

test.must_not_exist(test.workpath('work3', 'Test.dsp'))



test.pass_test()
