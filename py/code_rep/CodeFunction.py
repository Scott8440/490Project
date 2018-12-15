from py.code_rep.CodeBlock import CodeBlock
from py.code_rep.Variable import Variable

class CodeFunction(CodeBlock):

    def __init__(self, name, arguments, lineNumber, parentBlock=None):
        CodeBlock.__init__(self, lineNumber, blockType='func', parentBlock=parentBlock)
        self.name = name
        self.arguments = arguments
        for arg in self.arguments:
            equals = arg.find('=')
            if equals != -1:
                arg = arg[:arg.find('=')]  # Removes value after keyword argument
            var_names = [var.name for var in self.variables]
            if arg not in var_names:
                self.variables.append(Variable(arg, lineNumber))

    def getAccessedAttributes(self, attributeNames):
        accessedAttributes = set()
        for line in self.getAllLines():
            lineAttributes = line.getAccessedAttributes(attributeNames)
            accessedAttributes.update(lineAttributes)
        return accessedAttributes

    def printSelf(self, level=1):
        indent = "  "*level
        print("{} {}<Function: {} >".format(self.lineNumber, indent, self.name))
        print("{}    args: {}".format(indent, self.arguments))
        print("{}    Block Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}   {}{}".format(j.lineNumber, indent, j.line.strip()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
