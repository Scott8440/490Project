class CodeFunction:

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
        self.blocks = []
        self.lines = [] 

    def addChildBlock(self, block):
        self.blocks.append(block)

    def addLine(self, line):
        self.lines.append(line)

    def getLength(self):
        length = len(self.lines)
        for block in self.blocks:
            length += block.getLength()
        return length

    def printSelf(self, level=1):
        indent = "  "*level
        print("{}<Function: {} >: {}".format(indent, self.name, self.getLength()))
        print("{}  args: {}".format(indent, self.arguments))
        if self.lines:
            for j in self.lines:
                print("  {}{}".format(indent, j.strip()))
        for j in self.blocks:
            j.printSelf(level=level+1)
