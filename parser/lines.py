from MoinMoin.parser._ParserBase import ParserBase

Dependencies = ['user']

class Parser(ParserBase):

    Dependencies = Dependencies

    def setupRules(self):
        ParserBase.setupRules(self)
