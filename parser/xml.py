# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - XML Source Parser

    @copyright: 2005 by Davin Dubeau <davin.dubeau@gmail.com>
    @license: GNU GPL, see COPYING for details.
    
    @modified by Andrew Seigner <siggy@hotmail.com>

"""

from MoinMoin.parser._ParserBase import ParserBase

Dependencies = ['user']

class Parser(ParserBase):

    parsername = "ColorizedXML"
    extensions = ['.xml']
    Dependencies = Dependencies

    def setupRules(self):
        ParserBase.setupRules(self)
        return #disabled as this parser sucks

        self.addRulePair("Comment","<!--","-->")
        self.addRule("Number",r"[0-9]+")
        self.addRule("SPChar","[=<>/\"]")
        self.addRule("ResWord","(?!<)[\w\s]*(?![\w=\"])?(?![\w\s\.<])+(?!>)*")

        # new rules

        # tags
        self.addRulePair("ConsWord","<","[\s>]")
        
        # end tags
        self.addRule("ConsWord",">")
        
        # attributes in quotes
        self.addRulePair("SPChar","[\"]","[\"]")
        
        # special characters
        self.addRule("ResWord","[=/\"]")
        
        # comments
        self.addRulePair("Comment","<!--","-->")
