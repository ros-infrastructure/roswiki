# -*- coding: iso-8859-1 -*-
"""
  MoinMoin - Raw HTML Parser

  @copyright: 2010 by Chris Martino <chris@console.org>
  @license: GNU GPL.
"""

from MoinMoin.parser._ParserBase import ParserBase

Dependencies = ['user']

class Parser(ParserBase):

    parsername = "RawHTML"
    Dependencies = []

    def __init__(self, raw, request, **kw):
        self.raw = raw
        self.request = request

    def format(self, formatter):
        self.request.write(formatter.rawHTML(self.raw))
