from __future__ import with_statement
generates_headings = True
dependencies = []

import codecs
def macro_Contributors(macro):
    with codecs.open('/var/www/www.ros.org/contributors.html', 'r', encoding='utf-8') as f:
        return f.read()
