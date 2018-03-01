from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.FunctionAnalyzer import FunctionAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer


class ClassAnalyzer(CodeAnalyzer):

    def __init__(self, codeClass, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.codeClass = codeClass

    def analyzeClass(self):
        print("analyzing class")
        for codeFunction in self.codeClass.functions:
            print("Function: {}".format(codeFunction.name))
            functionAnalyzer = FunctionAnalyzer(codeFunction, parameters=self.params)
            functionAnalyzer.analyzeFunction()
            self.gatherAlerts(functionAnalyzer)

        for codeBlock in self.codeClass.childrenBlocks:
            blockAnalyzer = BlockAnalyzer(codeBlock, parameters=self.params)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.codeClass.lines:
            lineAnalyzer = LineAnalyzer(codeLine, parameters=self.params)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)



