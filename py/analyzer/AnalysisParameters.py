

class AnalysisParameters:

    def __init__(self):
        self.excludedMagicNumbers = [0, 1]
        self.variableScopeLengthRatio = 1
        # TODO: Move these into language-specific data object
        self.conditionalKeywords = ['and', 'or', '==', '!=', 'not', '>', '<']
        self.conditionalComplexityLimit = 2
        self.minNumberClassFunctionsForCohesionAnalysis = 5
        self.classCohesionLimit = 0.2

    def constructFromFile(self, filename):
        lines = []
        with open(filename) as paramFile:
            lines = paramFile.readlines()
        for line in lines:
            if self.paramLineMatches('Excluded Magic Numbers', line):
                self.excludedMagicNumbers = self.getArrayFromLine(line, valType=int)
            elif self.paramLineMatches('Variable Scope Length Ratio', line):
                self.variableScopeLengthRatio = self.getValueFromLine(line, valType=float)
            elif self.paramLineMatches('Conditional Keywords', line):
                self.conditionalKeywords = self.getArrayFromLine(line)
            elif self.paramLineMatches('Conditional Complexity Limit', line):
                self.conditionalComplexityLimit = self.getValueFromLine(line, valType=int)
            elif self.paramLineMatches('Minimum Number of Class Functions For Cohesion Analysis', line):
                self.minNumberClassFunctionsForCohesionAnalysis = self.getValueFromLine(line, valType=int)
            elif self.paramLineMatches('Class Cohesion Limit', line):
                self.classCohesionLimit = self.getValueFromLine(line, valType=float)

    def paramLineMatches(self, string, line):
        lineKey = line[0:line.find(':')].strip()
        return lineKey.lower() == string.lower()

    def getValueFromLine(self, line, valType=str):
        lineValue = valType(line[line.find(':')+1:].strip())
        return lineValue

    def getArrayFromLine(self, line, valType=str):
        lineValues = line[line.find(':')+1:].strip()
        returnArray = lineValues.split(', ')
        returnArray = [valType(element) for element in returnArray]
        return returnArray

    def setExcludedMagicNumbers(self, numbers):
        self.excludedMagicNumbers = numbers

    def setConditionalKeywords(self, keywords):
        self.conditionalKeywords = keywords

    def setConditionalComplexityLimit(self, limit):
        self.conditionalComplexityLimit = limit

    def setVariableScopeLengthRatio(self, ratio):
        self.variableScopeLengthRatio = ratio
