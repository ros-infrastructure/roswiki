# -*- coding: iso-8859-1 -*-
"""
    ROS - Glossary

    <<Glossary(term)>>
        Will produce this:

        <<Anchor(term)>>[#term|term]:

    @copyright: 2012 Willow Garage,
        William Woodall <wwoodall@willowgarage.com>
    @license: BSD
"""

from __future__ import print_function

import urllib

Dependencies = []


def execute(macro, args):
    if args:
        term = str(args)
        html = '<span class="anchor" id="{0}"</span><a href="#{0}">{1}</a>:'
        html = html.format(urllib.quote(term.replace(" ", "_")), term)
        return html
    else:
        return '`<<Anchor()>>` must be called with an argument.'

