from py.analyzer.CodeAlert import CodeAlert
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.CodeAnalyzer import CodeAnalyzer
import py.analyzer.AnalysisUtilies as utils


class LineAnalyzer(CodeAlert):

    def __init__(self, line):
        CodeAlert.__init__(self)
        self.line = line

    def checkForMagicNumbers(self):
        numberList = utils.extractMagicNumbers(self.line.line)
        lineNumber = self.line.lineNumber
        for number in numberList:
            if number in self.excludedMagicNumbers:
                continue
            self.addAlert(MagicNumberAlert(number, lineNumber))
