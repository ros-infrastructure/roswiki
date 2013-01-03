"""
MoinMoin figure parser

This is a shortcut for using section parser with class 'figure'

This plugin must be installed in the same directory as the section parser.

@copyright: 2005 by Nir Soffer <nirs@freeshell.org>
@license: GNU GPL, see COPYING for details.
"""

from section import SectionParser

class Parser(SectionParser):
    baseClass = 'figure'
