from py.CodeBlock import CodeBlock

class CodeFunction(CodeBlock):

    def __init__(self, name, arguments, lineNumber):
        CodeBlock.__init__(self, lineNumber, blockType='func')
        self.name = name
        self.arguments = arguments
        for arg in self.arguments:
            self.variables.add((arg, lineNumber))

    def printSelf(self, level=1):
        indent = "  "*level
        print("{} {}<Function: {} >".format(self.lineNumber, indent, self.name))
        print("{}    args: {}".format(indent, self.arguments))
        print("{}    Block Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}   {}{}".format(j.lineNumber, indent, j.line.strip()))
                print("     {}Vars: {}".format(indent, j.extractVariables()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
