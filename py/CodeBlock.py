class CodeBlock:

    def __init__(self, lineNumber, blockType=None):
        self.blockType = blockType
        self.variables = set() 
        self.lines = []
        self.childrenBlocks = []
        self.condition = None
        self.lineNumber=lineNumber

    def setType(self, blockType):
        self.blockType = blockType

    def addLine(self, line):
        self.lines.append(line)
        for var in line.extractVariables(): # Add variables as lines are added
            self.variables.add((var, line.lineNumber))

    def addChildBlock(self, block):
        #TODO: Should I add the parent block to the child? What can be gained from
        #       having access to the parent?
        self.childrenBlocks.append(block)

    def getLength(self):
        length = len(self.lines)
        for block in self.childrenBlocks:
            length += block.getLength()
        return length

    def printSelf(self, level=1):
        indent = "  "*level
        print("{}{}<{} Block>: {}".format(self.lineNumber,indent, self.blockType, self.getLength()))
        print("{}    Block Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}  {}{}".format(j.lineNumber, indent, j.line.strip()))
                print("    {}Vars: {}".format(indent, j.extractVariables()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
