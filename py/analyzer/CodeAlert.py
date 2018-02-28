

class CodeAlert:

    def __init__(self, lineText=''):
        self.alertType = ''
        self.lineNumber = 0
        self.alertDescription = ''
        self.fixText = ''
        self.lineText = lineText

    def setAlertType(self, alertType):
        self.alertType = alertType

    def setLineNumber(self, lineNumber):
        self.lineNumber = lineNumber

    def setAlertDescription(self, description):
        self.alertDescription = description

    def setFixText(self, fixText):
        self.fixText = fixText

    def toString(self):
        typeLine = "Alert: {}\n".format(self.alertType)
        lineNumberLine = "Line: {}".format(self.lineNumber)
        if self.lineText:
            lineNumberLine += ": {}\n".format(self.lineText.strip())
        else:
            lineNumberLine += "\n"
        descriptionLine = "{}\n".format(self.alertDescription)
        fixTextLine = "{}\n".format(self.fixText)

        return typeLine + lineNumberLine + descriptionLine + fixTextLine 
