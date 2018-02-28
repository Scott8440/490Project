from py.CodeFile import CodeFile
from py.CodeFunction import CodeFunction
from py.CodeClass import CodeClass
from py.CodeBlock import CodeBlock
from py.CodeLine import CodeLine


class FileAnalyzer:

    def __init__(self, codeFile):
        self.codeFile = codeFile

    def countFunctions(self):
        return len(codeFile.functions)

    def countBlocks(self):
        return len(codeFile.blocks)

    def countClasses(self):
        return len(codeFile.classes)

    def getFunctionNames(self):
        names = []
        for i in codeFile.functions:
            names.append(i.name)
        return names

    def getClassNames(self):
        names = []
        for i in codeFile.classes:
            names.append(i.name)
        return names
