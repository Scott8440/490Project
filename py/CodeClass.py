from py.CodeBlock import CodeBlock


class CodeClass(CodeBlock):

    def __init__(self, name, classParents, lineNumber):
        CodeBlock.__init__(self, lineNumber, blockType='class')
        self.name = name 
        self.parents = classParents
        self.memberFunctions = []

    def printSelf(self, level=1):
        indent = "  "*level
        print("{} {}<class: {} >".format(self.lineNumber, indent, self.name))
        print("{}    parents: {}".format(indent, self.parents))
        print("{}    memberVars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}   {}{}".format(j.lineNumber, indent, j.line.strip()))
                print("     {}Vars: {}".format(indent, j.extractVariables()))
        for j in self.memberFunctions:
            j.printSelf(level=level+1)
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)

