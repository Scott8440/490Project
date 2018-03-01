class CodeBlock:

    def __init__(self, lineNumber, parentBlock=None, blockType=None):
        self.blockType = blockType
        self.variables = {} 
        self.lines = []
        self.childrenBlocks = []
        self.condition = None
        self.lineNumber = lineNumber
        self.parentBlock = None
        if parentBlock:
            self.parentBlock = parentBlock


    def setType(self, blockType):
        self.blockType = blockType

    def addLine(self, line):
        self.lines.append(line)
        for var in line.extractVariables(): # Add variables as lines are added
            # self.variables.add((var, line.lineNumber))
            if (var not in self.variables.keys() and
                (not self.parentBlock or var not in self.parentBlock.variables.keys())):
                self.variables[var] = line.lineNumber

    def addChildBlock(self, block):
        self.childrenBlocks.append(block)

    def getLength(self):
        length = len(self.lines)
        for block in self.childrenBlocks:
            length += block.getLength()
        return length

    def getAllVariables(self):
        allVars = self.variables
        for block in self.childrenBlocks:
            # allVars = allVars.union(block.getAllVariables())
            allVars = {**allVars, **block.getAllVariables()}
        return allVars

    def printSelf(self, level=1):
        indent = "  "*level
        print("{}{}<{} Block>: {}".format(self.lineNumber, indent, self.blockType, self.getLength()))
        print("{}    Block Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}  {}{}".format(j.lineNumber, indent, j.line.strip()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
