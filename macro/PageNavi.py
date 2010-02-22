# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Navigation Macro

    @copyright: 2003 by Jürgen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.
"""

import re, string
from MoinMoin import config

from MoinMoin.Page import Page

Dependencies = ["namespace"]

def _getPages(request, pagename):
    """ Return a (filtered) list of pages names.
    """
    page = Page(request, pagename)
    #links = page.parsePageLinks(request)
    links = page.getPageLinks(request)
    return links

class Navigation:
    """ Dispatcher class implementing the navigation schemes.
    """

    # querystring for slideshow links
    PROJECTION = 'action=print&media=projection'

    def __init__(self, macro, args):
        """ Prepare common values used during processing.
        """
        self.macro = macro
        self.args = args.split(',')
        self._ = self.macro.request.getText

        self.pagename = self.macro.formatter.page.page_name
        self.print_mode = self.macro.request.form.has_key('action') \
            and self.macro.request.form['action'][0] == 'print'
        self.media = self.macro.request.form.get('media', [None])[0]
        self.querystr = self.print_mode and self.PROJECTION or ''

    def dispatch(self):
        """ Return None if in plain print mode (no navigational
            elements in printouts), else the proper HTML code.
        """

        return self.do_siblings(self.args[0])


    def do_siblings(self, parentPage, root=None):
        """ Navigate from a subpage to its siblings.
        """
        _ = self._

        # iterate over children, adding links to all of them
        result = []
        children = _getPages(self.macro.request, parentPage)
        for child in children:
            # display short page name, leaving out the parent path
            # (and make sure the name doesn't get wrapped)
            if child.startswith("Category"): continue
            shortname = child
            if child.startswith(parentPage):
              shortname = child[len(parentPage):]

            parts = string.split(child, "/")
            shortname = parts[-1]

            if not shortname: continue

            if child == self.pagename:
                # do not link to focus
                result.append(self.macro.formatter.text(shortname))
            else:
                # link to sibling / child
                result.append(Page(self.macro.request, child).link_to(self.macro.request, text=shortname))
#            result.append(' | ')

        return ' | '.join(result)




def execute(macro, args):
    # get HTML code with the links
    navi = Navigation(macro, args or '').dispatch()

    if navi:
        # return links packed into a table
        return navi

    # navigation disabled in plain print mode
    return ''

