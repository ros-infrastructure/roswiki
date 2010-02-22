# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Create an action link

    @copyright: 2004 by Johannes Berg <johannes@sipsolutions.de>
    @license: GNU GPL, see COPYING for details.
"""

import re

Dependencies = ["language"]
from MoinMoin import wikiutil

def execute(self, args):
  #TODO - check that template is valid

  result = wikiutil.link_tag(self.request, "%s?action=edit&amp;template=%s" % (
                        wikiutil.quoteWikinameURL(self.formatter.page.page_name),
                        wikiutil.quoteWikinameURL(args)), args)
  return result
