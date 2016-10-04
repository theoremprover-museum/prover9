#!/usr/bin/python

import sys
import re

if len(sys.argv) == 1:
    print "need n args: html-files"
    sys.exit(1)

fout = sys.stdout

html_files = sys.argv
html_files.pop(0)   # get rid of program name

refs = []

look = False

for file in html_files:

    outlines = '';

    fin = open(file)
    lines = fin.readlines()
    for line in lines:

        if re.search('<title>', line):
            page_name = line.split(': ')[1].split('<')[0]

        if re.match('<blockquote>', line) or re.match('<!-- end option', line):
            look = False

        if look:
            if re.match('<a name=', line):
                anchor_name = line.split('"')[1]
                ref = '<a href="%s#%s"><b>%s</b></a>' % (file,anchor_name,name)
                outlines += line
                refs.append((name,file))

            elif re.match('(assign|set)\(', line):
                ref_line = re.sub(name,ref,line)
                outlines += ref_line

            else:
                outlines += line

        if re.match('<!-- start option', line):
            name = line.split()[3]
            look = True

    if outlines != '':
        fout.write('<h3>From Page <a href="%s">%s</a></h3>\n\n' % (file,page_name))
        fout.write(outlines)

    fin.close()

fout = open('sed.option-refs', 'w')

for ref in refs:
    (name,file) = ref
    fout.write('s/<tt>%s<\/tt>/<a href="%s#%s"><tt><b>%s<\/b><\/tt><\/a>/\n' % (name,file,name,name))


