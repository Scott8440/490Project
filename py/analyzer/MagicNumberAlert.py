from py.analyzer.CodeAlert import CodeAlert


class MagicNumberAlert(CodeAlert):

    def __init__(self, number, lineNumber):
        CodeAlert.__init__()
        self.setAlertType("Magic Number")
        self.setLineNumber(lineNumber)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def writeDescription(self):
