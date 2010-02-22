#FORMAT python
"""
See the latex parser, this is just a thin wrapper around it.
"""
# Imports
from MoinMoin import wikiutil
import re

Dependencies = []

splitre = re.compile(r'([^\\])%')

class latex:
    def __init__(self, macro, args):
        self.macro = macro
        self.formatter = macro.formatter
        self.text = args
    
    def renderInPage(self):
        # return immediately if getting links for the current page
        if self.macro.request.mode_getpagelinks:
            return ''

        if self.text is None: # macro call without parameters
            return ''

        # get an exception? for moin before 1.3.2 use the following line instead:
        # L = wikiutil.importPlugin('parser', 'latex', 'Parser', self.macro.cfg.data_dir)
        L = wikiutil.importPlugin(self.macro.cfg, 'parser', 'latex', 'Parser')
        if L is None:
            return self.formatter.text("<<please install the latex parser>>")
        l = L('', self.macro.request)
        tmp = splitre.split(self.text, 1)
        if len(tmp) == 3:
            prologue,p2,tex=tmp
            prologue += p2
        else:
            prologue = ''
            tex = tmp[0]        
        return l.get(self.formatter, tex, prologue)


def execute(macro, args):
    return latex(macro, args).renderInPage()
