

class CodeAlert:

    def __init__(self):
        self.alertType = ''
        self.lineNumber = 0
        self.alertDescription = ''
        self.fixText = ''

    def setAlertType(self, alertType):
        self.alertType = alertType

    def setLineNumber(self, lineNumber):
        self.lineNumber = lineNumber

    def setAlertDescription(self, description):
        self.alertDescription = description

    def setFixText(self, fixText):
        self.fixText = fixText
