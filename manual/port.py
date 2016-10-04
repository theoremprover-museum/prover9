#!/usr/bin/python

# This Python script gets a list of portable-format LADR
# interpretations and just prints them in a different form.

import sys

interpretations = eval(sys.stdin.read())     # get interps from stdin

# interpretations = eval(file("LT-port.out").read())  # get interps from file

for interp in interpretations:

    [size, comments, operations] = interp

    for op in operations:

        [type, name, arity, values] = op

        print "\ntype=%s, name=%s, arity=%d, values=" % (type, name, arity)
        print values
    
