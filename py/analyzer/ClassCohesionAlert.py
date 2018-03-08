from py.analyzer.CodeAlert import CodeAlert


class ClassCohesionAlert(CodeAlert):

    def __init__(self, className, noAccessFunctions, lineNumber, lineText=''):
        CodeAlert.__init__(self, lineText=lineText)
        self.setAlertType("Class Cohesion")
        self.className = className
        self.noAccessFunctions = noAccessFunctions
        self.setLineNumber(lineNumber)
        self.setAlertDescription(self.writeDescription())
        self.setFixText(self.writeFixText())

    def writeDescription(self):
        description = "The class {} on line {} appears to be incohesive.\n".format(self.className, self.lineNumber)
        description += "{} of the functions in this class do not access or modify a member variable.\n".format(len(self.noAccessFunctions))
        description += "these functions are: "
        for func in self.noAccessFunctions:
            description += "{}, ".format(func) 
        description = description[:-2]
        return description

    def writeFixText(self):
        fixText = "You should consider breaking this class into multiple smaller classes."
        return fixText
