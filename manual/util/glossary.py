#!/usr/bin/python

import sys
import re

if len(sys.argv) == 1:
    print "need n args: glossary-file"
    sys.exit(1)

fout = sys.stdout

glossary_file = sys.argv[1]

refs = []
anchor = None
fout = open('sed.glossary', 'w')

fin = open(glossary_file)
lines = fin.readlines()

for line in lines:

    if re.search('<!-- start def', line):
        concept = re.sub('<!-- start def ', '', line)
        concept = re.sub(' -->\n', '', concept)
        refs.append(concept)

    if re.search('<a name="', line):
        anchor = re.sub('<a name="', '', line)
        anchor = re.sub('">\n', '', anchor)

        for ref in refs:
            fout.write('s/<g>%s<\/g>/<a href="%s#%s">%s<\/a>/\n' % (ref,glossary_file,anchor,ref))

        refs = []
        anchor = None



# for ref in refs:
#    (name,file) = ref
#    fout.write('s/<tt>%s<\/tt>/<a href="%s#%s"><tt><b>%s<\/b><\/tt><\/a>/\n' % (name,file,name,name))


