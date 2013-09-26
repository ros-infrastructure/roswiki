# -*- coding: iso-8859-1 -*-
"""
    ROS - TutorialChain

    <<TutorialChain(path/to/FirstTutorial)>>
        Given a wiki link to a Tutorial, it will traverse the next links
        until a terminal Tutorial with no next link is found. Then the
        Tutorials are displayed in order with links and descriptions.

    @copyright: 2012 Willow Garage,
        William Woodall <wwoodall@willowgarage.com>
    @license: BSD
"""

from __future__ import print_function

import re
from Queue import Queue

from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser

Dependencies = ["pages"]


def formatContext(page, macro):
    """ Format search context for each matched page

    Try to show first maxlines interesting matches context.
    """
    body = page.get_raw_body()

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

    return title, description, next_pages


def get_wiki_page(wiki_link, macro):
    if not wiki_link:
        return {}
    page_name = macro.formatter.page.page_name
    tutorial_page_name = wikiutil.AbsPageName(page_name, wiki_link)
    tutorial_page = Page(macro.request, tutorial_page_name)
    result = formatContext(tutorial_page, macro)
    if not result:
        return {}
    tutorial = {
        'link': tutorial_page_name,
        'title': result[0],
        'desc': result[1],
        'next': result[2]
    }
    return tutorial


def crawl_tutorials_breadth_first(tutorial_root, macro):
    queue = Queue()
    queue.put((tutorial_root, None))
    tutorials = []
    while not queue.empty():
        link, parent = queue.get()
        tut = get_wiki_page(link, macro)
        tup = (tut['link'], tut['title'], tut['desc'])
        if tut['link'] not in [t[0] for t in tutorials]:
            tutorials.append(tup)
        else:
            tutorials.append(tutorials.pop(tutorials.index(tup)))
        for next in tut['next']:
            queue.put((next, tut['link']))
    return tutorials


def execute(macro, first_tutorial):
    try:
        request = macro.request
        _ = request.getText

        if type(first_tutorial) == str:
            first_tutorial = first_tutorial.strip()
        if not first_tutorial:
            err = _('Invalid first Tutorial given: '
                    '{{{"%s"}}}', wiki=True) % first_tutorial
            return '<span class="error">%s</span>' % err

        tutorial_list = crawl_tutorials_breadth_first(first_tutorial, macro)

        f = macro.formatter
        content = ''
        content += f.number_list(1)
        for link, title, desc in tutorial_list:
            desc = desc or 'No Description'
            content += ''.join([
                f.listitem(1),
                f.pagelink(1, str(link or '#BadLink')),
                title or 'No Title',
                f.pagelink(0),
                "<p>",
                wikiutil.renderText(request, WikiParser, desc),
                "</p>",
                f.listitem(0)
            ])
        content += f.number_list(0)
        return content
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return '<span class="error"><pre>%s\nError: %s</pre></span>' % (tb, e)
