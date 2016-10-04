#!/usr/bin/python

import sys   # for argument processing and I/O.
import re    # regular expressions
import os

if len(sys.argv) != 3:
    print 'need 2 args: go-file html-file'
    sys.exit(1)

errors = 0

go_filename = sys.argv[1]
html_filename = sys.argv[2]

work_filename = html_filename + '.work'

work_file = open(work_filename, 'w')

go_file = open(go_filename)
lines = go_file.readlines()

job = None
jobs = {}

for line in lines:
    if re.match('# job', line):
        jobname = line.split()[2]
    
    elif re.search('\$d\/', line):
        # transform the command into HTML
        line = re.sub('\n', '', line)
        line = re.sub('\$d\/', '', line)
        line = re.sub('\$', '', line)

        html_name = line.split().pop() + '.html'   # last word + '.html'
        xml_name = line.split().pop() + '.xml'   # last word + '.xml'

        if os.access(html_name, os.F_OK):
            line = re.sub('$', ' ; ### ( %s )' % html_name , line)
        elif os.access(xml_name, os.F_OK):
            line = re.sub('$', ' ; ### ( %s )' % xml_name , line)

        line = re.sub(' > ', ' &gt; ', line)
        line = re.sub(' < ', ' &lt; ', line)
        line = re.sub('([^\s]*\.[^\s]*)', '<a href="\\1">\\1</a>', line)
        line = re.sub('^', '<blockquote><tt>', line)
        line = re.sub('$', '</tt></blockquote>', line)
        jobs[jobname] = line

go_file.close()

html_file = open(html_filename);
lines = html_file.readlines()

for line in lines:
    if re.match('<!-- job', line):
        jobname = line.split()[2]
        if jobname in jobs.keys():
            work_file.write(line)  # keep the marker in the HTML
            work_file.write(jobs[jobname] + '\n')
            del jobs[jobname]    # remove from dictionary
        else:
            sys.stderr.write('ERROR, not in the go file: %s\n' % jobname)
            errors += 1

    elif re.match('<blockquote>.*<\/blockquote>$', line):
        pass

    else:
        work_file.write(line)

html_file.close()

for k in jobs.keys():
    sys.stderr.write('ERROR, not in the HTML file: %s, %s\n' % (k, jobs[k]))
    errors += 1

if (errors != 0):
    sys.stderr.write('\nerrors=%d, file %s not changed\n' % (errors, html_filename))
    sys.stderr.write('partly constructed HTML in %s\n\n' % work_filename)
else:
    back_filename = html_filename + ".bak"
    os.rename(html_filename, back_filename)
    os.rename(work_filename, html_filename)
    sys.stderr.write('\nSuccess; file %s backed up to %s\n\n' % (html_filename, back_filename))
