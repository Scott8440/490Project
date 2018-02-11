class CodeClass:

    def __init__(self, name, classFunctions, classLines, lineNumber):
        self.name = name 
        self.memberVariables = []
        self.memberFunctions = classFunctions
        self.lines = classLines
        self.lineNumber = lineNumber
