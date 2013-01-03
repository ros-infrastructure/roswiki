# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - SHell Source Parser

    @copyright: 2009 Krzysztof Stryjek <wtps0n@bsdserwis.com>
    @license: GNU GPL, see COPYING for details.

"""

from MoinMoin.parser._ParserBase import ParserBase

Dependencies = ['user'] # the "Toggle line numbers link" depends on user's language

class Parser(ParserBase):

    parsername = "ColorizedShell"
    extensions = ['.shell']
    Dependencies = Dependencies

    def setupRules(self):
        ParserBase.setupRules(self)

        self.addRule("Comment", r"#.*$")
        self.addRulePair("String", r'"', r'$|[^\\](\\\\)*"')
        self.addRule("Char", r"'\\.'|'[^\\]'")
        self.addRule("Number", r"[0-9](\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?")
        self.addRule("ID", r"\$?[a-zA-Z_][0-9a-zA-Z_]*")
        self.addRule("SPChar", r"[~!$%^&*()+=|\[\]:;,.<>/?{}-]")

        reserved_words = ['echo', 'elif', 'until', 'in', 'alias','bg','fg',
        'builtin', 'cd', 'command', 'chdir', 'mkdir','eval', 'exec', 'exit',
        'export', 'fc', 'getopts',' jobid', 'hash', 'jobs', 'pwd', 'read', 'set',
        'readonly', 'setvar', 'shitf', 'test', 'trap', 'times', 'type', 'ulimit',
        'umask', 'unalias', 'unset', 'wait', 'bind',
        'if', 'else', 'fi', 'while', 'for', 'do', 'done', 'case', 'esac', 'then',
        'local', 'return', 'continue', 'break']

        self.addReserved(reserved_words)

        constant_words = ['true', 'false', ':']

        self.addConstant(constant_words)
