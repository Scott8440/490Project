from py.analyzer.CodeAlert import CodeAlert


class ConditionComplexityAlert(CodeAlert):

    def __init__(self, condition, lineNumber, lineText=''):
        CodeAlert.__init__(self, lineText=lineText)
        self.setAlertType("Condition Complexity")
        self.condition = condition
        self.setLineNumber(lineNumber)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def writeDescription(self):
        description = "The condition '{}' on line {} is too complex.".format(self.condition, self.lineNumber)
        return description

    def writeFixText(self):
        fixText = ("You should consider wrapping this condition in a well-named function "
                   "to make reading this conditional statement easier.")
        return fixText
