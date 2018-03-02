from py.analyzer.CodeAlert import CodeAlert


class MagicNumberAlert(CodeAlert):

    def __init__(self, number, lineNumber, lineText=''):
        CodeAlert.__init__(self, lineText=lineText)
        self.setAlertType("Magic Number")
        self.number = number
        self.setLineNumber(lineNumber)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def writeDescription(self):
        description = "There is a 'magic number' {} on line {}".format(self.number, self.lineNumber)
        return description

    def writeFixText(self):
        fixText = ("You should consider setting this number to be "
                          "a named constant and replacing all occurences of "
                          "the number with this constant.")
        return fixText
