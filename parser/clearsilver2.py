"""

    NEEDS REVIEW - refactor into Parser page

Hello World parser for MoinMoin wiki.

This hopefully gives a basic idea of what a parser looks like and what
the parts of it mean. 

Parsers are kind of in flux. The whole moinmoin thing is being refactored
a lot. But for right now, 1.3, Parsers sort of work like this:

A parser gets created by a Page object, is given the text its supposed
to format and an HTTPRequest object. It mucks around with the text,
and writes the result to the HTTPRequest object it was given. 

To install:

Copy this file into data/plugins/parser in your moinmoin wiki instance.
Restart the wiki if necessary.
Edit a page and type in

{{{#!HelloWorld 1 2 3
rabbit
}}}

The result should be something like this inserted in your page: 

hello world begin
raw: rabbit
kw: 1 2 3
hello world end


You can get more ideas by looking in the
'python\Lib\site-packages\MoinMoin\parser' directory on your computer,
or by looking at http://moinmoin.wikiwikiweb.de/ParserMarket
at the parsers that others have written. 
"""

from MoinMoin.Page import Page
from MoinMoin import wikiutil
from MoinMoin.parser.text_moin_wiki import Parser as WikiParser

import neo_cgi, neo_util, neo_cs

#from MoinMoin import wikiutil
#from MoinMoin.parser import wiki

class Parser:
    """ Hello World parser for MoinMoin wiki """
    
    def __init__(self, raw, request, **kw):
        # print "init"
        # 'init' is called once for each !# command but it doesnt do much.
        # Most of the work usually happens in the 'format' method.

        self.raw = raw
        # raw is the text inbetween the {{{ and }}} thingies. 
        # most parsers generally save it for use in the 'format'
        # method. 
        
        self.request = request
        # request is the HTTPRequest object
        # parsers generally save this during '__init__' for use later
        # on in 'format'. They have to write to it in fact to get
        # any results. 

        self.kw=kw
        # kw is is a dictionary with 'arguments' to the !# command.
        # for example: {{{!# HelloWorld a b c }}}
        # would give the following value for kw:
        # {'format_args': 'a b c '}

    def format(self, formatter):
        # print "format"
        # format is also called for each !# command. its called after __init__
        # is called. this is where parsers do most of their work.
        # they write their results into the Httprequest object
        # which is usually stored from __init__ in self.request. 
        
        # print "formatter",dir(formatter)
        # formatter is a special object in MoinMoin that
        # is supposed to help people who write extensions to have
        # sort of a uniform looking thing going on.
        # see http://moinmoin.wikiwikiweb.de/ApplyingFormatters?highlight=%28formatter%29
                
        # but formatter is not documented well. you have to look at
        # moinmoin/formatter/base.py. And if you do, you will see that half of
        # the methods raise a 'not implemented' error.
        # formatter is also being refactored alot so dont get used to it. 
        # if all else fails just use formatter.rawHTML which will
        # screw up XML output but at least it will work. 
 
        page_name = formatter.page.page_name
        cs_template_page = wikiutil.AbsPageName(page_name, self.kw["format_args"])
        cs_template = Page(self.request, cs_template_page).getPageText()

        hdf = neo_util.HDF()
        hdf.readString(self.raw.encode('utf8'))
        hdf.setValue("Config.WhiteSpaceStrip", "0")

        cs = neo_cs.CS(hdf)
        cs.parseStr(cs_template)
        body = cs.render()
        body = wikiutil.renderText(self.request, WikiParser, body.decode('utf8'))
        self.request.write(formatter.rawHTML(body))

        # the end

