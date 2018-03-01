from py.CodeFile import CodeFile
from py.analyzer.ClassAnalyzer import ClassAnalyzer
from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.FunctionAnalyzer import FunctionAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
from py.analyzer.MagicNumberAlert import MagicNumberAlert
from py.analyzer.MultiMagicNumberAlert import MultiMagicNumberAlert

class FileAnalyzer(CodeAnalyzer):

    def __init__(self, codeFile):
        CodeAnalyzer.__init__(self)
        self.codeFile = codeFile

    def analyzeFile(self):
        for codeClass in self.codeFile.classes:
            classAnalyzer = ClassAnalyzer(codeClass)
            classAnalyzer.analyzeClass()
            self.gatherAlerts(classAnalyzer)

        for codeFunction in self.codeFile.functions:
            functionAnalyzer = FunctionAnalyzer(codeFunction)
            functionAnalyzer.analyzeFunction()
            self.gatherAlerts(functionAnalyzer)

        for codeBlock in self.codeFile.blocks:
            blockAnalyzer = BlockAnalyzer(codeBlock)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.codeFile.lines:
            lineAnalyzer = LineAnalyzer(codeLine)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)

        self.consolidateMagicNumberAlerts()

    def consolidateMagicNumberAlerts(self):
        numberToAlerts = {}
        i = 0
        while i < len(self.alerts):
            alert = self.alerts[i]
            if isinstance(alert, MagicNumberAlert):
                del self.alerts[i]
                if alert.number in numberToAlerts.keys():
                    numberToAlerts[alert.number].append(alert)
                else:
                    numberToAlerts[alert.number] = [alert]
            else:
                i += 1
        for key in numberToAlerts.keys():
            if len(numberToAlerts[key]) > 1:
                self.addAlert(MultiMagicNumberAlert(numberToAlerts[key]))
            else:
                self.addAlert(numberToAlerts[key][0])

    def printAlerts(self):
        print("File: '{}' has {} warnings".format(self.codeFile.filename, len(self.alerts)))
        CodeAnalyzer.printAlerts(self)
