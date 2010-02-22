# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - Include macro

    This macro includes the formatted content of the given page(s). See

        http://purl.net/wiki/moinmaster/HelpOnMacros/Include

    for detailed docs.
    
    @copyright: 2000-2004 by Jürgen Hermann <jh@web.de>
    @copyright: 2000-2001 by Richard Jones <richard@bizarsoftware.com.au>
    @license: GNU GPL, see COPYING for details.
"""

#Dependencies = ["pages"] # included page
Dependencies = ["time"] # works around MoinMoinBugs/TableOfContentsLacksLinks

import re, StringIO
from MoinMoin import wikiutil
from MoinMoin.Page import Page
from MoinMoin.util import web

_sysmsg = '<p><strong class="%s">%s</strong></p>'

## keep in sync with TableOfContents macro!
_arg_heading = r'(?P<heading>,)\s*(|(?P<hquote>[\'"])(?P<htext>.+?)(?P=hquote))'
_arg_level = r',\s*(?P<level>\d*)'
_arg_from = r'(,\s*from=(?P<fquote>[\'"])(?P<from>.+?)(?P=fquote))?'
_arg_to = r'(,\s*to=(?P<tquote>[\'"])(?P<to>.+?)(?P=tquote))?'
_arg_sort = r'(,\s*sort=(?P<sort>(ascending|descending)))?'
_arg_items = r'(,\s*items=(?P<items>\d+))?'
_arg_skipitems = r'(,\s*skipitems=(?P<skipitems>\d+))?'
_arg_titlesonly = r'(,\s*(?P<titlesonly>titlesonly))?'
_arg_editlink = r'(,\s*(?P<editlink>editlink))?'
_args_re_pattern = r'^(?P<name>[^,]+)(%s(%s)?%s%s%s%s%s%s%s)?$' % (
    _arg_heading, _arg_level, _arg_from, _arg_to, _arg_sort, _arg_items,
    _arg_skipitems, _arg_titlesonly, _arg_editlink)

_title_re = r"^(?P<heading>\s*(?P<hmarker>=+)\s.*\s(?P=hmarker))$"

def extract_titles(body, title_re):
    titles = []
    for title, _ in title_re.findall(body):
        h = title.strip()
        level = 1
        while h[level:level+1] == '=': level = level+1
        depth = min(5,level)
        title_text = h[level:-level].strip()
        titles.append((title_text, level))
    return titles

def execute(macro, text, args_re=re.compile(_args_re_pattern), title_re=re.compile(_title_re, re.M), called_by_toc=0):
    request = macro.request
    _ = request.getText

    # return immediately if getting links for the current page
    if request.mode_getpagelinks:
        return ''

    # parse and check arguments
    args = text and args_re.match(text)
    if not args:
        return (_sysmsg % ('error', _('Invalid include arguments "%s"!')) % (text,))

    # prepare including page
    result = []
    print_mode = macro.form.has_key('action') and macro.form['action'][0] in ("print", "format")
    this_page = macro.formatter.page
    if not hasattr(this_page, '_macroInclude_pagelist'):
        this_page._macroInclude_pagelist = {}

    # get list of pages to include
    inc_name = wikiutil.AbsPageName(request, this_page.page_name, args.group('name'))
    pagelist = [inc_name]
    if inc_name.startswith("^"):
        try:
            inc_match = re.compile(inc_name)
        except re.error:
            pass # treat as plain page name
        else:
            # Get user filtered readable page list
            pagelist = request.rootpage.getPageList(filter=inc_match.match)

    # sort and limit page list
    pagelist.sort()
    sort_dir = args.group('sort')
    if sort_dir == 'descending':
        pagelist.reverse()
    max_items = args.group('items')
    if max_items:
        pagelist = pagelist[:int(max_items)]

    skipitems = 0
    if args.group("skipitems"):
        skipitems = int(args.group("skipitems"))
    titlesonly = args.group('titlesonly')
    editlink = args.group('editlink')

    # iterate over pages
    for inc_name in pagelist:
        if not request.user.may.read(inc_name):
            continue
        if this_page._macroInclude_pagelist.has_key(inc_name):
            result.append(u'<p><strong class="error">Recursive include of "%s" forbidden</strong></p>' % (inc_name,))
            continue
        if skipitems:
            skipitems -= 1
            continue
        fmt = macro.formatter.__class__(request, is_included=True)
        fmt._base_depth = macro.formatter._base_depth
        inc_page = Page(request, inc_name, formatter=fmt)
        if not inc_page.exists():
            continue
        inc_page._macroInclude_pagelist = this_page._macroInclude_pagelist

        # check for "from" and "to" arguments (allowing partial includes)
        body = inc_page.get_raw_body() + '\n'

#        body = body.replace(this_page.page_name, "_" + this_page.page_name + "_")
        body = body.replace('amcl', "_" + this_page.page_name + "_")

        # set or increment include marker
        this_page._macroInclude_pagelist[inc_name] = \
            this_page._macroInclude_pagelist.get(inc_name, 0) + 1

        # output the included page
        strfile = StringIO.StringIO()
        request.redirect(strfile)
        try:
            cid = request.makeUniqueID("Include_%s" % wikiutil.quoteWikinameURL(inc_page.page_name))
            inc_page.send_page(request, content_only=1, content_id=cid,
                               omit_footnotes=True)
            result.append(strfile.getvalue())
        finally:
            request.redirect()

        # decrement or remove include marker
        if this_page._macroInclude_pagelist[inc_name] > 1:
            this_page._macroInclude_pagelist[inc_name] = \
                this_page._macroInclude_pagelist[inc_name] - 1
        else:
            del this_page._macroInclude_pagelist[inc_name]


    # return include text
    str = ''.join(result)
    return str

# vim:ts=4:sw=4:et
