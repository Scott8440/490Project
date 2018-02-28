from py.CodeFunction import CodeFunction
from py.CodeLine import CodeLine
from py.CodeBlock import CodeBlock
from py.analyzer.CodeAnalyzer import CodeAnalyzer


class FunctionAnalyzer(CodeAnalyzer):

    def __init__(self, codeFunction, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.function = codeFunction

    def analyzeFunction(self):
        pass

    def countArgs(self):
        return len(self.function.args)

    def countBlocks(self):
        return len(self.function.blocks)

    def countTopLevelLines(self):
        return len(self.function.lines)

    def countTotalLines(self):
        return self.function.getLength()

    def getTopLevelVariables(self):
        return self.function.variables

    def getAllVariables(self):
        return self.function.getAllVariables()
