from py.parser.CodeBlock import CodeBlock
from py.parser.CodeFunction import CodeFunction


class CodeClass(CodeBlock):

    def __init__(self, name, classParents, lineNumber, parentBlock=None):
        CodeBlock.__init__(self, lineNumber, blockType='class', parentBlock=parentBlock)
        self.name = name 
        self.parents = classParents
        self.functions = []
        self.memberVariables = [] # Variables which are available to entire class

    def addChildBlock(self, block):
        if isinstance(block, CodeFunction):
            self.addFunction(block)
        else:
            self.addChildBlock(block)

    def addLine(self, line):
        self.lines.append(line)
        for var in line.extractVariables(): # Add variables as lines are added
            if (var not in self.variables.keys() and
                (not self.parentBlock or var not in self.parentBlock.variables.keys())):
                self.variables[var] = line.lineNumber
            if 'self.' in var:
                self.memberVariables.append(var)

    def addFunction(self, function):
        self.functions.append(function)
        for var in function.variables:
            if 'self.' in var:
                self.memberVariables.append(var)

    def getFunction(self, functionName):
        for func in self.functions:
            if func.name == functionName:
                return func

    def getFunctionNames(self):
        names = []
        for func in self.functions:
            names.append(func.name)
        return names

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

