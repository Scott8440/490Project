from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.FunctionAnalyzer import FunctionAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer


class ClassAnalyzer(CodeAnalyzer):

    def __init__(self, codeClass, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.codeClass = codeClass

    def analyzeClass(self):
        for codeFunction in self.codeClass.functions:
            functionAnalyzer = FunctionAnalyzer(codeFunction)
            functionAnalyzer.analyzeFunction()
            self.gatherAlerts(functionAnalyzer)

        for codeBlock in self.codeClass.childrenBlocks:
            blockAnalyzer = BlockAnalyzer(codeBlock)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.codeClass.lines:
            lineAnalyzer = LineAnalyzer(codeLine)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)



