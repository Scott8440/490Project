class CodeBlock:

    def __init__(self, blockType=None):
        self.blockType = blockType
        self.variables = []
        self.lines = []
        self.childrenBlocks = []

    def addLine(self, line):
        self.lines.append(line)

    def addChildBlock(self, block):
        self.childrenBlocks.append(block)
