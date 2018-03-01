

class AnalysisParameters:

    def __init__(self):
        self.excludedMagicNumbers = [0, 1]
        self.variableScopeLengthRatio = 1

    def setExcludedMagicNumbers(self, numbers):
        self.excludedMagicNumbers = numbers
