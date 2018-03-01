from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.VariableNameLengthAlert import VariableNameLengthAlert
import py.analyzer.AnalysisUtilities as utils


class BlockAnalyzer(CodeAnalyzer):
    
    def __init__(self, block, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.block = block

    def analyzeBlock(self):
        for line in self.block.lines:
            lineAnalyzer = LineAnalyzer(line, parameters=self.params)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)

        if self.block.condition:
            self.analyzeCondition()
        self.analyzeVariables()

    def analyzeCondition(self):
        if not self.block.condition:
            return 
        magicNumbers = utils.extractMagicNumbers(self.block.condition)
        for number in magicNumbers:
            if number in self.params.excludedMagicNumbers:
                continue
            self.addAlert(MagicNumberAlert(number, self.block.lineNumber))

    def analyzeVariables(self):
        blockScope = self.block.getLength()
        for variable in self.block.variables.keys():
            if len(variable)/blockScope < self.params.variableScopeLengthRatio:
                self.addAlert(VariableNameLengthAlert(variable, blockScope, self.block.variables[variable]))


