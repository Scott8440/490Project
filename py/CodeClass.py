class CodeClass:

    def __init__(self, name, classFunctions, classParents, classLines, lineNumber):
        self.name = name 
        self.memberVariables = []
        self.memberFunctions = classFunctions
        self.lines = classLines
        self.lineNumber = lineNumber
        self.parents = classParents
