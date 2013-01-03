# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Navigation Macro

    @copyright: 2003 by Jürgen Hermann <jh@web.de>
    @license: GNU GPL, see COPYING for details.
"""

import re, string
from MoinMoin import config

from MoinMoin.Page import Page

from MoinMoin import log
logging = log.getLogger(__name__)

Dependencies = ["namespace"]

from MoinMoin.formatter.pagelinks import Formatter

class MyFormatter(Formatter):
    """ Collect pagelinks and format nothing :-) """
    def __init__(self, request, store_pagelinks):
      Formatter.__init__(self, request, store_pagelinks=store_pagelinks)

      self._text = []

    def pagelink(self, on, pagename='', page=None, **kw):
      #logging.log(logging.INFO, "link == %s %s %s" % (pagename, repr(on), repr(self._text)))

      if not self._store_pagelinks or on or kw.get('generated'):
        self._text = []
        return self.null()

      if not pagename and page:
          pagename = page.page_name
      #pagename = self.request.normalizePagename(pagename)
      if pagename and pagename not in self.pagelinks:
        if self._text:
          linktext = string.join(self._text)
        else:
          linktext = 'Link'

        self.pagelinks.append((pagename, linktext))

      self._text = []

      return self.null()

    def null(self, *args, **kw):
        return ''


    # All these must be overriden here because they raise
    # NotImplementedError!@#! or return html?! in the base class.
    set_highlight_re = rawHTML = url = image = smiley = text = null
    strong = emphasis = underline = highlight = sup = sub = strike = null
    code = preformatted = small = big = code_area = code_line = null
    code_token = linebreak = paragraph = rule = icon = null
    number_list = bullet_list = listitem = definition_list = null
    definition_term = definition_desc = heading = table = null
    table_row = table_cell = attachment_link = attachment_image = attachment_drawing = null
    transclusion = transclusion_param = null

    def text(self, s, **kw):
      self._text.append(s)
      return ''
      
  

class MyPage(Page):
  def myparsePageLinks(self, request):
        pagename = self.page_name
        if request.parsePageLinks_running.get(pagename, False):
            #logging.debug("avoid recursion for page %r" % pagename)
            return [] # avoid recursion

        #logging.debug("running parsePageLinks for page %r" % pagename)
        # remember we are already running this function for this page:
        request.parsePageLinks_running[pagename] = True

        request.clock.start('parsePageLinks')

        class Null:
            def write(self, data):
                pass

        request.redirect(Null())
        request.mode_getpagelinks += 1
        try:
            try:
                formatter = MyFormatter(request, store_pagelinks=1)
                page = MyPage(request, pagename, formatter=formatter)
                page.send_page(content_only=1)
            except:
                logging.exception("pagelinks formatter failed, traceback follows")
        finally:
            request.mode_getpagelinks -= 1
            #logging.debug("mode_getpagelinks == %r" % request.mode_getpagelinks)
            request.redirect()
            if hasattr(request, '_fmt_hd_counters'):
                del request._fmt_hd_counters
            request.clock.stop('parsePageLinks')
        return formatter.pagelinks
  

def _getPages(request, pagename):
    """ Return a (filtered) list of pages names.
    """
    page = MyPage(request, pagename)
    #links = page.parsePageLinks(request)
    #links = page.getPageLinks(request)
    links = page.myparsePageLinks(request)
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
        for child, linktext in children:
            # display short page name, leaving out the parent path
            # (and make sure the name doesn't get wrapped)
            if child.startswith("Category"): continue
            shortname = child
            if child.startswith(parentPage):
              shortname = child[len(parentPage):]

            parts = string.split(child, "/")

            if linktext:
              shortname = linktext
            else:
              shortname = parts[-1]

            if not shortname: continue

            if child == self.pagename:
                # do not link to focus
                result.append(self.macro.formatter.text(shortname))
            else:
                # link to sibling / child
                result.append(Page(self.macro.request, child).link_to(self.macro.request, text=shortname))

        if len(result) >= 2:
          str = self.macro.formatter.strong(1) + self.macro.formatter.emphasis(1) + result[0] + self.macro.formatter.strong(0) + ": " + ' | '.join(result[1:]) + self.macro.formatter.emphasis(0)
        else:
          str = ' | '.join(result)

        # wrap up the nav menu in a span so it's easier for rosmanual to find
        if len(str) > 0:
          str = self.macro.formatter.span(1, css_class="macro-nav-menu") + str + self.macro.formatter.span(0) + "\n"

        return str




def execute(macro, args):
    # get HTML code with the links
    navi = Navigation(macro, args or '').dispatch()

    if navi:
        # return links packed into a table
        return navi

    # navigation disabled in plain print mode
    return ''

