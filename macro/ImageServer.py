# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - YouTube macro Version 0.1
               Displays an emended object with the wanted video

    <<YouTube(YouTubeID)>>
    Exampel: <<YouTube(2SXKM-dLJV8)>>

    @copyright: 2008 by MarcelHäfner (www.heavy.ch)
    @license: GNU GPL, see COPYING for details.

"""

import re, StringIO
from MoinMoin import wikiutil
_sysmsg = '<p><strong class="%s">%s</strong></p>'

def execute(macro, args):
    if not args:
       return (_sysmsg % ('error', 'Missing You!',))

    params = args.split(",")

    link = "%s" % (wikiutil.escape(params[0]),)
    width = params[1]
    height = params[2]
    

##    html= '''<a href="http://photos.willowgarage.com/photos/show/%(link)s"><img src="http://photos.willowgarage.com/photos/file/%(link)s?sz=%(width)s,%(height)s" width=%(width)s height=%(height)s style="display:block; float:right;"></a>''' % locals()
    html= '''<a href="http://photos.willowgarage.com/photos/show/%(link)s"><img src="http://photos.willowgarage.com/photos/file/%(link)s?sz=%(width)s,%(height)s" width=%(width)s height=%(height)s style="display:block;"></a>''' % locals()

    return macro.formatter.rawHTML(html)

