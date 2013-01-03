# -*- coding: iso-8859-1 -*-
"""MoinMoin - IncludeWikiContent

A macro to include another wiki page content with the context set to the current
page. This Inclusion is not recursive (included pages won't get their
IncludeWikiContent macro evaluated).

Usage:
    Use this macro to include common elements of your wiki, such as standard
    subpages, headers etc...

Syntax:
    <<IncludeWikiContent(include page name)>>

"""

from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser


# do not cache
Dependencies = ["namespace"]


def execute(macro, args):
    request = macro.request
    content = []
    page_name = macro.formatter.page.page_name

    # get args
    include_page_name = ''
    if args is not None:
        include_page_name = args

    include_page_name = wikiutil.AbsPageName(page_name, include_page_name)

    include_page = Page(request, include_page_name)

    if include_page is None:
        return ''
    if not request.user.may.read(include_page_name):
        return ''
    else:
        return wikiutil.renderText(request, WikiParser, include_page.getPageText())
