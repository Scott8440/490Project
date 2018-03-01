from py.CodeBlock import CodeBlock
from py.CodeFunction import CodeFunction


class CodeClass(CodeBlock):

    def __init__(self, name, classParents, lineNumber):
        CodeBlock.__init__(self, lineNumber, blockType='class')
        self.name = name 
        self.parents = classParents
        self.functions = []

    def addChildBlock(self, block):
        if isinstance(block, CodeFunction):
            self.addFunction(block)
        else:
            self.addChildBlock(block)

    def addFunction(self, function):
        self.functions.append(function)

    def printSelf(self, level=1):
        indent = "  "*level
        print("{} {}<class: {} >".format(self.lineNumber, indent, self.name))
        print("{}    Parents: {}".format(indent, self.parents))
        print("{}    Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}   {}{}".format(j.lineNumber, indent, j.line.strip()))
        for j in self.functions:
            j.printSelf(level=level+1)
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)

