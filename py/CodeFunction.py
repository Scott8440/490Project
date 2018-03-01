from py.CodeBlock import CodeBlock

class CodeFunction(CodeBlock):

    def __init__(self, name, arguments, lineNumber):
        CodeBlock.__init__(self, lineNumber, blockType='func')
        self.name = name
        self.arguments = arguments
        for arg in self.arguments:
            equals = arg.find('=')
            if equals != -1:
                arg = arg[:arg.find('=')] # Removes value after keyword argument
            # self.variables.add((arg, lineNumber))
            if arg not in self.variables.keys():
                self.variables[arg] = lineNumber

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
