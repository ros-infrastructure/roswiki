# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - MenuLink Macro

    [[MenuLink(left)]]

"""

def execute(macro, args):
  if len(args) == 2:
    pagename = args[0]
    name = args[1]
  else:
    pagename = args
    name = args

  if pagename == macro.request.page.page_name:
    return name
  else:
    return macro.formatter.pagelink(1, pagename) + name + macro.formatter.pagelink(0, pagename)

