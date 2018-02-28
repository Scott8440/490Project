from py.CodeFunction import CodeFunction
from py.CodeLine import CodeLine
from py.CodeBlock import CodeBlock


class FunctionAnalyzer:

    def __init__(self, codeFunction):
        self.function = codeFunction

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
