from py.analyzer.CodeAlert import CodeAlert


class MultiMagicNumberAlert(CodeAlert):

    def __init__(self, magicNumberAlerts):
        CodeAlert.__init__(self)
        self.setAlertType("Magic Numbers")
        self.number = magicNumberAlerts[0].number
        self.setLineNumber(magicNumberAlerts[0].lineNumber)
        self.lineNumberList = []
        self.getLineNumberList(magicNumberAlerts)
        self.numOccurrences = len(magicNumberAlerts)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def getLineNumberList(self, alertList):
        for alert in alertList:
            self.lineNumberList.append(alert.lineNumber)

    def writeDescription(self):
        description = "There are {} occurrences of a 'magic number' {} on lines ".format(self.numOccurrences, self.number)
        for i in self.lineNumberList:
            description += str(i) + ", "
        description = description[:-2]
        return description

    def writeFixText(self):
        fixText = ("You should consider setting this number to be "
                   "a named constant and replacing all occurences of "
                   "the number with this constant.")
        return fixText
