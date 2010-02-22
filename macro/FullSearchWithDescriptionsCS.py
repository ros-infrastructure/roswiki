# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FullSearch Macro

    <<FullSearch>>
        displays a search dialog, as it always did.

    <<FullSearch()>>
        does the same as clicking on the page title, only that
        the result is embedded into the page. note the '()' after
        the macro name, which is an empty argument list.

    <<FullSearch(Help)>>
        embeds a search result into a page, as if you entered
        'Help' into the search box.

    The macro creates a page list without context or match info, just
    like PageList macro. It does not make sense to have context in non
    interactive search, and this kind of search is used usually for
    Category pages, where we don't care about the context.

    TODO: If we need to have context for some cases, either we add a context argument,
          or make another macro that uses context, which may be easier to use.

    @copyright: 2000-2004 Juergen Hermann <jh@web.de>,
                2006 MoinMoin:FranzPletz
    @license: GNU GPL, see COPYING for details.
"""

import re
from MoinMoin import wikiutil, search

from MoinMoin.parser import text_moin_wiki as wiki
import string, StringIO

Dependencies = ["pages"]


def search_box(type, macro):
    """ Make a search box

    Make both Title Search and Full Search boxes, according to type.

    @param type: search box type: 'titlesearch' or 'fullsearch'
    @rtype: unicode
    @return: search box html fragment
    """
    _ = macro._
    if 'value' in macro.form:
        default = wikiutil.escape(macro.form["value"][0], quote=1)
    else:
        default = ''

    # Title search settings
    boxes = ''
    button = _("Search Titles")

    # Special code for fullsearch
    if type == "fullsearch":
        boxes = [
            u'<br>',
            u'<input type="checkbox" name="context" value="160" checked="checked">',
            _('Display context of search results'),
            u'<br>',
            u'<input type="checkbox" name="case" value="1">',
            _('Case-sensitive searching'),
            ]
        boxes = u'\n'.join(boxes)
        button = _("Search Text")

    # Format
    type = (type == "titlesearch")
    html = [
        u'<form method="get" action="%s/%s">' % (macro.request.getScriptname(), wikiutil.quoteWikinameURL(macro.request.formatter.page.page_name)),
        u'<div>',
        u'<input type="hidden" name="action" value="fullsearch">',
        u'<input type="hidden" name="titlesearch" value="%i">' % type,
        u'<input type="text" name="value" size="30" value="%s">' % default,
        u'<input type="submit" value="%s">' % button,
        boxes,
        u'</div>',
        u'</form>',
        ]
    html = u'\n'.join(html)
    return macro.formatter.rawHTML(html)

def pageListWithContext(self, macro, request, formatter, info=1, context=180,
                        maxlines=1, paging=True, hitsFrom=0, hitsInfo=0):
    """ Format a list of found pages with context

    The default parameter values will create Google-like search
    results, as this is the most known search interface. Good
    interface is familiar interface, so unless we have much better
    solution (we don't), being like Google is the way.

    @param request: current request
    @param formatter: formatter to use
    @param info: show match info near the page link
    @param context: how many characters to show around each match.
    @param maxlines: how many contexts lines to show.
    @param paging: toggle paging
    @param hitsFrom: current position in the hits
    @param hitsInfo: toggle hits info line
    @rtype: unicode
    @return formatted page list with context
    """
    self._reset(request, formatter)
    f = formatter
    write = self.buffer.write
    _ = request.getText

    if paging and len(self.hits) <= request.cfg.search_results_per_page:
        paging = False

    if len(self.hits) == 0:
      write(f.definition_list(1) + f.definition_term(1) + "No results found." + f.definition_term(0) + f.definition_list(0))      
    # Add pages formatted as definition list
    else:
        write(f.number_list(1))

        if paging:
            hitsTo = hitsFrom + request.cfg.search_results_per_page
            displayHits = self.hits[hitsFrom:hitsTo]
        else:
            displayHits = self.hits

        display_results = []

        for page in displayHits:
            # TODO handle interwiki search hits
            matchInfo = ''
            next_page = None
            if info:
                matchInfo = self.formatInfo(f, page)
            if page.attachment:
                fmt_context = ""
                querydict = {
                    'action': 'AttachFile',
                    'do': 'view',
                    'target': page.attachment,
                }
            elif page.page_name.startswith('FS/'): # XXX FS hardcoded
                fmt_context = ""
                querydict = None
            else:
                title, fmt_context, next_pages = formatContext(self, macro, page, context, maxlines)
                if page.rev and page.rev != page.page.getRevList()[0]:
                    querydict = {
                        'rev': page.rev,
                    }
                else:
                    querydict = None
            querystr = self.querystring(querydict)
            item = [
                f.listitem(1),
#                f.pagelink(1, page.page_name, querystr=querystr),
                f.pagelink(1, page.page_name),
                title,
                f.pagelink(0),
                "<p>", 
                fmt_context,
                "</p>",
                f.listitem(0),
                ]
            display_results.append((page.page_name, next_pages, ''.join(item)))

        sorted_display_results = sortResults(display_results)

        for node in sorted_display_results:
          write(node.body)
        write(f.number_list(0))
        if paging:
            write(self.formatPageLinks(hitsFrom=hitsFrom,
                hitsPerPage=request.cfg.search_results_per_page,
                hitsNum=len(self.hits)))

    return self.getvalue()


 
class Node:  
  def __init__(self, pagename, body, dependencies):  
    self.pagename = pagename  
    self.body = body  
    self.dependencies = dependencies
 
  def __repr__(self): 
    return "<Node %s %s>" % (self.pagename, self.dependencies) 
 
def topoSort(dependencies): 
  dead = {} 
  list = [] 
 
  for node in dependencies.values():  dead[node] = False 

  nonterminals = []
  terminals = []
  for node in dependencies.values():
    if node.dependencies:
      nonterminals.append(node)
    else:
      terminals.append(node)
 
  for node in nonterminals:
    visit(dependencies, terminals, node, list, dead); 
 
  list.reverse()

  list = list + terminals
  return list 
 
def visit(dependencies, terminals, dependency, list, dead): 
  if dependency is None: return
  if dead.get(dependency, False): return 
 
  dead[dependency] = True 
 
  if dependency.dependencies: 
    for node in dependency.dependencies:
      visit(dependencies, terminals, dependencies.get(node, None), list, dead) 
  try:
    terminals.remove(dependency)
  except ValueError: pass

  list.append(dependency) 
 
def sortResults(display_results):  
  dependencies = {}  
 
  for pagename, nextpages, body in display_results:  
    node = Node(pagename, body, nextpages) 
    dependencies[pagename] = node 
 
  results = topoSort(dependencies) 
 
  return results 

    

def formatContext(self, macro, page, context, maxlines):
    """ Format search context for each matched page

    Try to show first maxlines interesting matches context.
    """
    f = self.formatter
    if not page.page:
        page.page = Page(self.request, page.page_name)
    body = page.page.get_raw_body()
    last = len(body) - 1
    lineCount = 0
    output = ""
    next_page = None

    pagedict = {}
    for line in body.split("\n"):
      if line.startswith("##"):
        line = line[2:].strip()
        parts = line.split("=", 1)
        if len(parts) == 2:
          pagedict[parts[0].strip()] = parts[1].strip()

    title = pagedict.get("title", "No Title")
    description = pagedict.get("description", "No Description")

    next_pages = []
    linkpat = re.compile("\[\[([^|]*)(\|([^]]*))?\]\]")
    for key,val in pagedict.items():
      if key.startswith("next.") and key.find(".link") != -1:
        m = linkpat.search(val)
        if m:
          next_pages.append(m.group(1))

    if description:
      out=StringIO.StringIO()
      macro.request.redirect(out)
      wikiizer = wiki.Parser(description, macro.request)
      wikiizer.format(macro.formatter)
      description=out.getvalue()
      macro.request.redirect()
      del out

    return title, description, next_pages

def execute(macro, needle):
    request = macro.request
    _ = request.getText

    # if no args given, invoke "classic" behavior
    if needle is None:
        return search_box("fullsearch", macro)

    # With empty arguments, simulate title click (backlinks to page)
    elif needle == '':
        needle = '"%s"' % macro.formatter.page.page_name

    # With whitespace argument, show error message like the one used in the search box
    # TODO: search should implement those errors message for clients
    elif needle.isspace():
        err = _('Please use a more selective search term instead of '
                '{{{"%s"}}}', wiki=True) % needle
        return '<span class="error">%s</span>' % err

    needle = needle.strip()

    # Search the pages and return the results
    results = search.searchPages(request, needle, sort='page_name')
    return pageListWithContext(results, macro, request, macro.formatter, paging=False)


    ret = []
    for result in results:
      pass

    return string.join(ret)


