class CodeBlock:

    def __init__(self, blockType=None):
        self.blockType = blockType
        self.variables = []
        self.lines = []
        self.childrenBlocks = []
        self.condition = None

    def addLine(self, line):
        self.lines.append(line)

    def addChildBlock(self, block):
        self.childrenBlocks.append(block)

    def getLength(self):
        length = len(self.lines)
        for block in self.childrenBlocks:
            length += block.getLength()
        return length
        
    def printSelf(self, level=1):
        indent = "  "*level
        print("{}<{} Block>: {}".format(indent, self.blockType, self.getLength()))
        if self.lines:
            #print("{}LINES:".format(indent))
            for j in self.lines:
                print("  {}{}".format(indent, j.strip()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
