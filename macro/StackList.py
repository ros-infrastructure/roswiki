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
from StackNavi import macro_StackNavi
from MoinMoin.parser import text_moin_wiki as wiki
import string, StringIO

Dependencies = ["pages"]



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

        if paging:
            hitsTo = hitsFrom + request.cfg.search_results_per_page
            displayHits = self.hits[hitsFrom:hitsTo]
        else:
            displayHits = self.hits

        display_results = []

        for page in displayHits:
            f.div(0, css_class='content')
            write(macro_StackNavi(macro, page.page_name))

    return getvalue(self)

def getvalue(self):
    """ Return output in div with CSS class """
    value = [
        self.formatter.div(1, css_class='content'),
        self.buffer.getvalue(),
        self.formatter.div(0),
        ]
    return '\n'.join(value)


 
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

    
def execute(macro, needle):
    request = macro.request
    _ = request.getText

    # With whitespace argument, show error message like the one used in the search box
    # TODO: search should implement those errors message for clients
    if needle.isspace():
        err = _('Please use a more selective search term instead of '
                '{{{"%s"}}}', wiki=True) % needle
        return '<span class="error">%s</span>' % err

    needle = needle.strip()
 
    # Search the pages and return the results
    if(needle=='all'):
      results = search.searchPages(request, 'CategoryStack -StackList -StackTemplate', sort='page_name')
    else:
      lookfor= needle + ' CategoryStack -StackList -StackTemplate'
      results = search.searchPages(request, lookfor, sort='page_name')
    return pageListWithContext(results, macro, request, macro.formatter, paging=False)


    ret = []
    for result in results:
      pass

    return string.join(ret)


