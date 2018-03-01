from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer


class FunctionAnalyzer(CodeAnalyzer):

    def __init__(self, codeFunction, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.function = codeFunction

    def analyzeFunction(self):
        for codeBlock in self.function.childrenBlocks:
            blockAnalyzer = BlockAnalyzer(codeBlock, parameters=self.params)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.function.lines:
            lineAnalyzer = LineAnalyzer(codeLine, parameters=self.params)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)
        allVars = self.getAllVariables()

    def getAllVariables(self):
        print(self.function.getAllVariables())
        return self.function.getAllVariables()
