from py.CodeBlock import CodeBlock


class CodeClass(CodeBlock):

    def __init__(self, name, classParents, lineNumber):
        self.name = name 
        self.memberVariables = []
        self.memberFunctions = classFunctions
        self.lines = classLines
        self.lineNumber = lineNumber
        self.parents = classParents
