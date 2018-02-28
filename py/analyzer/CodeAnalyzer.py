from py.analyzer.AnalysisParameters import AnalysisParameters

class CodeAnalyzer:

    def __init__(self, parameters=None):
        self.alerts = []
        if parameters:
            self.params = parameters
        else:
            self.params = AnalysisParameters()

    def addAlert(self, alert):
        self.alerts.append(alert)

    def getAlerts(self):
        return self.alerts

    def gatherAlerts(self, analyzer):
        for alert in analyzer.alerts:
            self.addAlert(alert)

    def printAlerts(self):
        for alert in self.alerts:
            print(alert.toString())
