from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.VariableNameLengthAlert import VariableNameLengthAlert
from py.analyzer.ConditionComplexityAlert import ConditionComplexityAlert
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
        self.checkConditionComplexity()

    def checkConditionComplexity(self):
        condition = self.block.condition
        keywords = self.params.conditionalKeywords
        keywordCount = 0
        for word in keywords:
            keywordCount += condition.count(word)
        if keywordCount > self.params.conditionalComplexityLimit:
            self.addAlert(ConditionComplexityAlert(condition, self.block.lineNumber))

    def analyzeVariables(self):
        blockScope = self.block.getLength()
        for variable in self.block.variables.keys():
            if len(variable)/blockScope < self.params.variableScopeLengthRatio:
                self.addAlert(VariableNameLengthAlert(variable, blockScope, self.block.variables[variable]))


