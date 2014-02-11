#!/usr/bin/env python

import optparse
import os
import re


def add_rel_canonical(f, canonical_base='http://wiki.ros.org'):
    if not os.path.exists(f):
        print('cannot find %s' % f)
        return

    with open(f, 'r') as fh:
        lines = []
        for l in fh:
            lines.append(l)

        head_line_num = None
        backlink_line = None
        count = 0
        for l in lines:
            count += 1
            if '<head>' in l:
                head_line_num = count
            if 'backlink' in l:
                backlink_line = l

        if not backlink_line:
            print('Failed to find backlink line, skipping file %s' % f)
            return

        pattern = '.+<a class="backlink">(.+)</a>'
        #print "pattern, backlink_line", pattern, backlink_line
        result = re.match(pattern, backlink_line)

        if not result:
            print('Error regexing backlink in file %s' % f)
            return

        name = result.groups(1)[0]
        #print "match = %s"%name
        #print name
        link_line = '<link rel="canonical" href="%s/%s"/>\n' % (canonical_base, name)

        if head_line_num:
            lines.insert(head_line_num, link_line)
            with open(f, 'w') as outfile:
                for l in lines:
                    outfile.write(l)

        else:
            print('no <head> element found')
            return

parser = optparse.OptionParser()

(opts, args) = parser.parse_args()

if len(args) != 1:
    parser.error("Expected 1 argument got %d: [%s]" % (len(args), args))

d = args[0]
if not os.path.isdir(d):
    parser.error("argument is not a directory %s" % d)

html_files = set()

files = os.listdir(d)
for f in [f for f in files if f.endswith('html')]:
    html_files.add(os.path.join(d, f))


for f in html_files:
    print('processing %s' % f)
    add_rel_canonical(f)
