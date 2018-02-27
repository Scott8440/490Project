class CodeFile:

    def __init__(self):
        self.filename = ''
        self.functions = []
        self.classes = []
        self.blocks = []
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)

    def addChildBlock(self, block):
        self.blocks.append(block)

    def addFunction(self, block):
        self.functions.append(block)

    def addClass(self, block):
        self.classes.append(block)
