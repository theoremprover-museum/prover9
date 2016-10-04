#!/usr/bin/python

import sys   # for argument processing and I/O.
import re    # regular expressions
import os

if len(sys.argv) != 2:
    print 'need 1 args: go-file'
    sys.exit(1)


go_filename = sys.argv[1]
go_file = open(go_filename)

lines = go_file.readlines()

jobnames = []
title = None

for line in lines:
    if (re.match('# NAME', line)):
        title = re.sub('# NAME ', '', line)
        title = re.sub('\n', '', title)
        
    elif re.match('# job', line):
        jobname = line.split()[2]
        jobnames.append(jobname)
    

go_file.close()

sys.stdout.write( """<html>
<title>%s</title>
<body>

<h1>%s</h1>
""" % (title,title))

for job in jobnames:
    sys.stdout.write("\n<!-- job %s -->\n" % job)

sys.stdout.write( "\n</body>\n</html>\n" )


