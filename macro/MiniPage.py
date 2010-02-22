# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - MiniPage Macro

    PURPOSE:
        This macro is used to get the possibility to write inside a wiki table normal wiki code.
	This code is parsed by the wiki parser and is then displayed.

    CALLING SEQUENCE:
        [[MiniPage(wikicode)]]

    INPUTS:
        wikicode: e.g. * item1
    EXAMPLE:
       ||Buttons ||[[MiniPage( * Redo\n * Undo)]][[MiniPage( * Quit)]]||
       ||Section ||[[MiniPage(= heading 1 =)]][[MiniPage(== heading 2 ==)]]||

    PROCEDURE:
       The \n mark is used for a line break.

       Please remove the Version number from the code!

    MODIFICATION HISTORY:
        Version 1.3.3.-1
        Version 1.3.3.-2 Updated for Moin1.6
        @copyright: 2007 by Reimar Bauer (R.Bauer@fz-juelich.de)
        @license: GNU GPL, see COPYING for details.

"""
from MoinMoin.parser import text_moin_wiki as wiki
#from MoinMoin.parser import wiki
import string, StringIO

def execute(macro, text):
     text=string.replace(string.join(text, ''), '\\n', '\n')

     out=StringIO.StringIO()
     macro.request.redirect(out)
     wikiizer = wiki.Parser(text, macro.request)
     wikiizer.format(macro.formatter)
     result=out.getvalue()
     macro.request.redirect()
     del out
     return(result)
