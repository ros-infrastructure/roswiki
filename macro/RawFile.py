# -*- coding: iso-8859-1 -*-

import os, string, mimetypes
from MoinMoin import wikiutil
from MoinMoin.action import AttachFile
 
def execute(macro, text):
  kw = {}
  if text:
    args=text.split(',')
  else:
    args=[]

  fn = args[0]
  desc = fn
  if len(args) >= 2:
    desc = args[1]

  return '<a href="?action=AttachFile&do=raw&target=%s">%s</a>' % (fn, desc)


