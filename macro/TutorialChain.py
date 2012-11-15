# -*- coding: iso-8859-1 -*-
"""
    ROS - TutorialChain

    <<TutorialChain(<FirstTutorial>)>>
        Given a wiki link to a Tutorial, it will traverse the next links
        until a terminal Tutorial with no next link is found. Then the
        Tutorials are displayed in order with links and descriptions.

    @copyright: 2012 Willow Garage, William Woodall <wwoodall@willowgarage.com>
    @license: BSD
"""

import re
import StringIO

from MoinMoin.parser import text_moin_wiki as wiki


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
    for key, val in pagedict.items():
        if key.startswith("next.") and key.find(".link") != -1:
            m = linkpat.search(val)
            if m:
                next_pages.append(m.group(1))

    if description:
        out = StringIO.StringIO()
        macro.request.redirect(out)
        wikiizer = wiki.Parser(description, macro.request)
        wikiizer.format(macro.formatter)
        description = out.getvalue()
        macro.request.redirect()
        del out

    return title, description, next_pages


def get_wiki_page(wiki_link):
    return {}


def crawl_tutorials(tutorial_list):
    # Check to see if the latest tutorial exists
    tutorial = get_wiki_page(tutorial_list[-1][0])
    if not tutorial:
        return tutorial_list
    # Update the list
    tutorial_list[-1] = (tutorial['link'], tutorial['desc'])
    # Add the next one
    tutorial_list.append((tutorial['next'], 'Page Not Found'))
    # Recurse
    return crawl_tutorials(tutorial_list)


def execute(macro, first_tutorial):
    request = macro.request
    _ = request.getText

    head = first_tutorial
    if type(head) == str:
        head = head.strip()
    if not head:
        err = _('Invalid first Tutorial given: '
                '{{{"%s"}}}', wiki=True) % head
        return '<span class="error">%s</span>' % err

    tutorial_list = [(head, 'Page Not Found')]
    tutorial_list = crawl_tutorials(tutorial_list)

    return tutorial_list
