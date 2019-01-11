#! /usr/bin/env python3
#
# transmogrify.py - transform as if by magic, ok, tis just a simplified macroprocessor in python
#
'''This file provides a simple python3 based macro using string.Template and generated code. 

The gentle reader might ask why, when there are a large number of libraries like this,
well this one is pretty simple and I did look. This is based on a TCL version which
is kind of cool and minimalist.
'''

main_opts = '''
Usage: transmogrifier [-d] [<inputs>...]

Options:
   <inputs>    Input files
   -d          Turn debuggering on [default: False]
'''

import docopt
import sys

def main():
    global main_opts
    options = docopt.docopt(main_opts)
    # print(options)
    process_files(options['<inputs>'])

def process_files(fns):
    if fns == []:
        process_fd(sys.stdin)
    else:
        for fn in fns:
            process_fd(open(fn, 'r'))

def process_fd(fd):
    process(fd.readlines())

def process_str(s):
    return process(s.splitlines())

r = '**NONE*'
def process(ls):
    c = parse(ls)
    # print(c)
    exec(c, globals(), locals())
    print(r, end='')
    return r
        
from string import Template

def parse(ls):
    '''returns a program for ls'''
    prog = 'global r' + '\n'
    prog += 'r = ""\n'
    for l in ls:
        indent = leading_ws(l)
        if is_code(l):
            prog += expand_code(l)
        else: # literal
            prog += indent + 'r += ' + 'expand_literal(' + repr(following_ws(l)) + ',{**globals(), **locals()})' + '\n'
    return prog

def expand_literal(s, d):
    t = Template(s)
    r =  t.substitute(d)
    if False:
        print('expand_literal', s)
        for n in d:
            print(n, d[n])
        print('returns', r)
    return r

def expand_code(s):
    '''expand s as a piece of code'''
    return leading_ws(s) + s[s.index('%')+1:]

def is_code(s):
    '''True off this line is a code line
    >>> assert is_code('% ...')
    >>> assert is_code('    %...')
    '''
    for c in s:
        if c == '%':
            return True
        elif c.isspace():
            pass
        else:
            return False
        
def leading_ws(s):
    '''return a string containing the leading whitespace for s

    >>> assert leading_ws('') == ''
    >>> assert leading_ws(' a') == ' '
    >>> assert leading_ws(' ' * 5 + 'a') == ' ' * 5
    '''
    r = ''
    for c in s:
        if c.isspace():
            r += c
        else:
            break
    return r

def following_ws(s):
    for i, c in enumerate(s):
        if not c.isspace():
            return s[i:]
    return ''

def index_leading_non_ws(s):
    for i, c in emnumerate(s):
        if not c.isspace():
            return i
    return -1

if False:
    from hypothesis import given, note, assume, Verbosity
    import hypothesis.strategies as st
    from hypothesis import settings

    ts = settings(max_examples=1000,
              deadline=1000,
              derandomize=True,
              database=None,
              verbosity=Verbosity.verbose)
    @settings(ts)
    @given(st.from_regex(r'\A[^\r].*\Z'))
    def test_id(s):
        print(s, '->', process_str(s))
        assume (s.lstrip() != '') # sorry but whitespace only is broken. well uhmmm...
        assert s.lstrip() == process_str(s)

if False:
    for c in ['', 'hello']:
        assert process_str(c) == c

if __name__ == '__main__':
    main()
    
