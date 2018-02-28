from py.CodeFile import CodeFile
from py.analyzer.ClassAnalyzer import ClassAnalyzer
from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.FunctionAnalyzer import FunctionAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer

class FileAnalyzer(CodeAnalyzer):

    def __init__(self, codeFile):
        CodeAnalyzer.__init__(self)
        self.codeFile = codeFile

    def analyzeFile(self):
        for codeClass in self.codeFile.classes:
            classAnalyzer = ClassAnalyzer(codeClass)
            classAnalyzer.analyzeClass()
            self.gatherAlerts(classAnalyzer)

        for codeFunction in self.codeFile.functions:
            functionAnalyzer = FunctionAnalyzer(codeFunction)
            functionAnalyzer.analyzeFunction()
            self.gatherAlerts(functionAnalyzer)

        for codeBlock in self.codeFile.blocks:
            blockAnalyzer = BlockAnalyzer(codeBlock)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.codeFile.lines:
            lineAnalyzer = LineAnalyzer(codeLine)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)
