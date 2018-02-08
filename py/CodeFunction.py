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
