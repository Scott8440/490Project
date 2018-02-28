from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
import py.analyzer.AnalysisUtilities as utils

class BlockAnalyzer(CodeAnalyzer):
    
    def __init__(self, block, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.block = block

    def analyzeBlock(self):
        for line in self.block.lines:
            lineAnalyzer = LineAnalyzer(line)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)

        if self.block.condition:
            self.analyzeCondition()

    def analyzeCondition(self):
        if not self.block.condition:
            return 
        magicNumbers = utils.extractMagicNumbers(self.block.condition)
        for number in magicNumbers:
            if number in self.params.excludedMagicNumbers:
                continue
            self.addAlert(MagicNumberAlert(number, self.block.lineNumber))


