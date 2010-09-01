# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Navigation Macro

    @copyright: 2003 by Jürgen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.
"""

import re, string
from MoinMoin import config

Dependencies = []

def execute(macro, args):
    # get HTML code with the links
    if args and args != 'end':
      return macro.formatter.span(1, css_class="macro-nav-menu")
    else:
      return macro.formatter.span(0)

