# Import a RSS Feed into MoinMoin
# Ian Wienand <ianw@ieee.org>
# (C) 2006 - Public Domain

# Using this macro
# [[RSSReader(url[,allow_html])]]
# where
# * url is the url of the RSS/ATOM feed to read
# * allow_html is an optional argument if you trust the feed to put
#   the HTML directly into the page

# CAUTION: this could be an attack vector, although feedparser should
# strip most "bad" HTML.

# this tells MoinMoin not to cache the page, as we don't know when it
# changes.
Dependencies = ["time"]

from MoinMoin import util, wikiutil, config
from MoinMoin.Page import Page

class RSStoWiki:
    def __init__(self, macro, url, allow_html):
        self.macro = macro
        self.fmt = macro.formatter
        self.allow_html = allow_html
        # in debian package python-feedparser
        import feedparser
        self.f = feedparser.parse(url)
        self.result = []
        if self.f.feed == {}:
            self.result.append (self.fmt.icon('info') + \
                                self.fmt.strong(1) + \
                                self.fmt.text(' Unable to retreive feed %s' % url) + \
                                self.fmt.strong(0))
            self.valid = False
        else:
            self.valid = True
                          

    def get_title(self):
        if not self.f.feed.has_key('title'):
            return
        self.result.append(self.fmt.heading(on=1, depth=1) + \
                           self.fmt.text(self.f.feed.title) + \
                           self.fmt.heading(on=0, depth=1))

    def get_subtitle(self):
        if not self.f.feed.has_key('subtitle'):
            return
        self.result.append(self.fmt.heading(on=1, depth=2) + \
                           self.fmt.text(self.f.feed.subtitle) + \
                           self.fmt.heading(on=0, depth=2))

    def get_paragraph(self, text):
        self.result.append(self.fmt.paragraph(on=1) + \
                           self.fmt.text(text) + \
                           self.fmt.paragraph(on=0))

    def get_link(self, link):
        self.result.append(self.fmt.url(on=1, href=link) + \
                           self.fmt.icon('www') + \
                           self.fmt.text(" "+link) + \
                           self.fmt.url(on=0))
        
    def get_feedlink(self):
        if not self.f.feed.has_key('link'):
            return
        self.get_link(self.f.feed.link)

    def get_description(self):
        if not self.f.feed.has_key('description'):
            return
        self.get_paragraph(self.f.feed.description)

    def get_rule(self):
        self.result.append(self.fmt.rule(size=1))

    def get_entry_header(self, title):
        self.result.append(self.fmt.heading(on=1, depth=3) + \
                           self.fmt.text(title) + \
                           self.fmt.heading(on=0, depth=3))

    def get_entry_body(self, body):
        self.result.append(self.fmt.paragraph(on=1))
        if (self.allow_html):
            self.result.append(self.fmt.rawHTML(body))
        else:
            self.result.append(self.fmt.text(body))
        self.result.append(self.fmt.paragraph(on=0))

    def get_entries(self):
        for entry in self.f.entries:
            if entry.has_key('title'):
                self.get_entry_header(entry.title)
            if entry.has_key('updated'):
                self.get_paragraph(entry.updated)
            if entry.has_key('description'):
                self.get_entry_body(entry.description)
            if entry.has_key('link'):
                self.get_link(entry.link)

    def get_output(self):
        if self.valid:
            self.get_title()
            self.get_subtitle()
            self.get_description()
            self.get_feedlink()
            self.get_rule()
            self.get_entries()
            self.get_rule()
        return ''.join(self.result)

def execute(macro, args):
    macro_args = args.split(",")
    try:
        if macro_args[1].strip() == "allow_html":
            allow_html = True
        else:
            allow_html = False
    except:
        allow_html = False

    rss = RSStoWiki(macro, macro_args[0], allow_html)
    return rss.get_output()
