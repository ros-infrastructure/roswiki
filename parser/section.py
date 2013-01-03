"""
MoinMoin section parser
=======================

The parser is used to treat content as a page within a page. The section
have a header and a body, using the same format as moin regular
page. Only some of the headers are supported of course.

supported headers
-----------------
#format - any moin parser name
#class - any class name. The rendered class will be 'section value'
#language - any language known to moin

Bugs
----

'pragma section-number' is not supported as enabling this in the section
cause section number to display in the page. To fix this request state
or maybe formatter state should be saved before rendering the section
and then resotored.

Other headers are ignored.


@copyright: 2005 by Nir Soffer <nirs@freeshell.org>
@license: GNU GPL, see COPYING for details.
"""

import re
from MoinMoin import wikiutil, i18n, error

# This module is not part of MoinMoin currently, need to install this
from MoinMoin.util.header import Header


class SectionHeader(Header):
    """ Customization for sections headers """
    def set_class(self, value):
        """ Save multiple values for class """
        try:
            self._headers['class'].append(value)
        except KeyError:
            self._headers['class'] = [value]


class SectionParser:

    # One can use "inline:sidebar.section" to insert a section from an
    # attachment.
    extensions = ['.section']
    
    # allow caching
    caching = 1
    Dependencies = []

    baseClass = 'section'
    
    def __init__(self, text, request, **keywords):
        # Required undocumented attribtues, used by wikimacro
        self.form = request.form

        # Private attribtues
        self.text = text
        self.request = request
        self.keyswords = keywords

    def format(self, formatter):
        """ Formatter the text inside classed div """
        self.header = SectionHeader(self.request, self.text)
        Parser = self.importParser(self.sectionFormat())
        parser = Parser(self.text[self.header.length():], self.request)

        # Set content language during rendering
        savedLanguage = self.request.content_lang
        self.request.setContentLanguage(self.sectionLanguage())
        try:
            # XXX Should use formatter.section when its available
            self.request.write(formatter.rawHTML(
                    '<div class="%s">\n' % self.sectionClass()))       
            parser.format(formatter)        
            self.request.write(formatter.rawHTML('</div>\n'))       
        finally:
            self.request.setContentLanguage(savedLanguage)

    # ------------------------------------------------------------------
    # Private

    def sectionClass(self):
        """ Return class list starting with base class """
        classes = [self.baseClass] + self.header.get('class', [])
        return ' '.join(classes)

    def sectionFormat(self):
        format = self.header.get('format', 'wiki')
        # Prevent infinite recursion
        if format == 'section':
            format = 'wiki'
        return format

    def sectionLanguage(self):
        return self.header.get('language', self.request.content_lang)
    
    # This stuff is also needed by SlideShow, so it should not be part
    # of action or parser code. Seems that this should be part of
    # wikiutil, or maybe in some plugin module.

    def importParser(self, name):
        Parser = importPlugin(self.request.cfg, 'parser', name, 'Parser')
        if Parser is None:
            from MoinMoin.parser.text_moin_wiki import Parser
        return Parser


def importPlugin(cfg, kind, name, function="execute"):
    """ Import plugin supporting both new and old error handling

    To port old plugins to new moin releases, copy this into your plugin
    and use it instead of wikiutil.importPlugin. Your code would run on
    both 1.3 and later.
    """
    if hasattr(wikiutil, 'PluginMissingError'):
        # New error handling: missing plugins ignored, other errors in
        # plugin code will be raised.
        try:
            Plugin = wikiutil.importPlugin(cfg, kind, name, function)
        except wikiutil.PluginMissingError:
            Plugin = None
    else:
        # Old error handling: most errors in plugin code will be hidden.
        Plugin = wikiutil.importPlugin(cfg, kind, name, function)

    return Plugin


Parser = SectionParser
