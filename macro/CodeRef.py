# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - CodeRef Macro

    <<CodeRef(blockname,start_line,end_line)>>

"""

from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser
from MoinMoin.parser import text_moin_wiki as wiki

import re, string, StringIO


# do not cache
Dependencies = ["namespace"]

def execute(macro, args):
    args = args.split(',')
    if len(args) != 3:
      return "invalid arguments: <<CodeRef(blockname,start_line,end_line)>>"

    block = args[0]
    start_line = int(args[1])
    end_line = int(args[2])

    if not block: 
      return "invalid arguments: no code block specified"
    if start_line > end_line:
      return "invalid arguments: start_line cannot be greater than end_line."

    request = macro.request
    content = []
    page_name = macro.formatter.page.page_name
    

    page = Page(request, page_name)
    body = page.get_raw_body()
    
    start_pat = re.compile("{{{\n(#!.*)\n")
    block_pat = re.compile("block=([-a-z0-9_]*)")
    end_pat = re.compile("}}}")
    i = 0
    code_block = None
    specline = None
    while i<len(body):
      m = start_pat.search(body, i)
      if m is None: break

      if m:
        specline = m.group(1)
        m2 = block_pat.search(specline)
        if m2:
          _block = m2.group(1)
          if block == _block:
            m3 = end_pat.search(body, m.end())
            if m3:
              code_block = body[m.end():m3.start()]
            else:
              code_block = "unknown"
            break
      i = m.end()

    if not code_block:
      return "Error: No code_block found"

    lines = code_block.split("\n")
    mylines = lines[start_line-1:end_line]
    code_block = string.join(mylines, "\n")

    out=StringIO.StringIO()
    macro.request.redirect(out)
    wikiizer = wiki.Parser("{{{\n"+specline + " start=%d" % start_line + "\n" + code_block+"\n}}}\n", macro.request)
    wikiizer.format(macro.formatter)
    result=out.getvalue()
    macro.request.redirect()
    del out

    return result


