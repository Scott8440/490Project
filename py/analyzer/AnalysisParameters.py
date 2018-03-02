

class AnalysisParameters:

    def __init__(self):
        self.excludedMagicNumbers = [0, 1]
        self.variableScopeLengthRatio = 1
        self.conditionalKeywords = ['and', 'or', '==', '!=', 'not', '>', '<']
        self.conditionalComplexityLimit = 2
        self.minNumberClassFunctionsForCohesionAnalysis = 5
        self.classCohesionLimit = 0.2

    def setExcludedMagicNumbers(self, numbers):
        self.excludedMagicNumbers = numbers

    def setConditionalKeywords(self, keywords):
        self.conditionalKeywords = keywords

    def setConditionalComplexityLimit(self, limit):
        self.conditionalComplexityLimit = limit

    def setVariableScopeLengthRatio(self, ratio):
        self.variableScopeLengthRatio = ratio
