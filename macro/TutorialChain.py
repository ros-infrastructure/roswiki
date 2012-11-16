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

import re

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


def crawl_tutorials(tutorial_list, macro):
    # Update the list
    for i in reversed(range(len(tutorial_list))):
        if tutorial_list[i][1] is not None:
            break  # Hit a filled out tutorial, the rest should be too
        # Check to see if the latest tutorial exists
        tutorial = get_wiki_page(tutorial_list[i][0], macro)
        if not tutorial:
            continue  # Failed to get the page, don't update it
        tutorial_list[i] = (
            tutorial['link'],
            tutorial['title'],
            tutorial['desc']
        )
    # Add the next one
    next_tutorials = set(list(tutorial['next']))
    if len(next_tutorials) == 0:
        return tutorial_list
    for next in next_tutorials:
        tutorial_list.append((next, None, None))
    # Recurse
    return crawl_tutorials(tutorial_list, macro)


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

        tutorial_list = [(first_tutorial, None, None)]
        tutorial_list = crawl_tutorials(tutorial_list, macro)

        f = macro.formatter
        content = ''
        content += f.number_list(1)
        for link, title, desc in tutorial_list:
            desc = str(desc or 'No Description')
            content += ''.join([
                f.listitem(1),
                f.pagelink(1, str(link or '#BadLink')),
                str(title or 'No Title'),
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
