from py.CodeFunction import CodeFunction
from py.CodeLine import CodeLine
from py.CodeBlock import CodeBlock
from py.analyzer.CodeAlert import CodeAlert
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.CodeAnalyzer import CodeAnalyzer
import re


class LineAnalyzer(CodeAlert):

    def __init__(self, line):
        CodeAlert.__init__(self)
        self.line = line 

    def checkForMagicNumbers(self):
        strippedText = self.line.removeStrings()
        lineNumber = self.line.lineNumber

        numberList = re.findall(r"\d+", strippedText)

        for number in numberList:
            if number in self.excludedMagicNumbers:
                continue
            alert = MagicNumberAlert(number, lineNumber)
            self.addAlert(MagicNumberAlert)



