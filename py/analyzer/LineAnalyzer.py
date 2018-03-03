from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.CodeAnalyzer import CodeAnalyzer
import py.analyzer.AnalysisUtilities as utils


class LineAnalyzer(CodeAnalyzer):

    def __init__(self, line, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.line = line

    def analyzeLine(self):
        self.checkForMagicNumbers()

    def checkForMagicNumbers(self):
        numberList = utils.extractMagicNumbers(self.line.stripLine())
        lineNumber = self.line.lineNumber
        for number in numberList:
            if number in self.params.excludedMagicNumbers:
                continue
            self.addAlert(MagicNumberAlert(number, lineNumber, lineText=self.line.line))
