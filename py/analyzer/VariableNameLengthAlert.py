from py.analyzer.CodeAlert import CodeAlert


class VariableNameLengthAlert(CodeAlert):

    def __init__(self, variable, scope, lineNumber, lineText=''):
        CodeAlert.__init__(self, lineText=lineText)
        self.setAlertType("Variable Name Length")
        self.variable = variable
        self.variableScope = scope
        self.setLineNumber(lineNumber)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def writeDescription(self):
        varLine = "You have defined a variable with too short of a name on line {}.\n".format(self.lineNumber)
        lengthLine = "The variable '{}' has a length of {}, but has a scope of {} lines.\n".format(self.variable, len(self.variable), self.variableScope)
        descLine = "Variables with a large scope should be more descriptive than those with short scopes"
        return varLine + lengthLine + descLine

    def writeFixText(self):
        fixText = ("You should consider renaming this variable to be "
                   "longer and more descriptive.")
        return fixText
