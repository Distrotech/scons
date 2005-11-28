"""SCons.Tool.latex

Tool-specific initialization for LaTeX.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""

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

import SCons.Action
import SCons.Defaults
import SCons.Scanner.LaTeX
import SCons.Util
import SCons.Tool
import SCons.Tool.tex

LaTeXAction = SCons.Action.Action('$LATEXCOM', '$LATEXCOMSTR')

def LaTeXAuxFunction(target = None, source= None, env=None):
    SCons.Tool.tex.InternalLaTeXAuxAction( LaTeXAction, target, source, env )

LaTeXAuxAction = SCons.Action.Action(LaTeXAuxFunction, strfunction=None)

def generate(env):
    """Add Builders and construction variables for LaTeX to an Environment."""

    try:
        bld = env['BUILDERS']['DVI']
    except KeyError:
        bld = SCons.Defaults.DVI()
        env['BUILDERS']['DVI'] = bld

    bld.add_action('.ltx', LaTeXAuxAction)
    bld.add_action('.latex', LaTeXAuxAction)
    bld.add_emitter('.ltx', SCons.Tool.tex.tex_emitter)
    bld.add_emitter('.latex', SCons.Tool.tex.tex_emitter)

    env['LATEX']        = 'latex'
    env['LATEXFLAGS']   = SCons.Util.CLVar('')
    env['LATEXCOM']     = '$LATEX $LATEXFLAGS $SOURCES'
    env['LATEXRETRIES'] = 3

def exists(env):
    return env.Detect('latex')
