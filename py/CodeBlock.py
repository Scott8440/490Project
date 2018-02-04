class CodeBlock:

    def __init__(self):
        self.variables = []
        self.lines = []
        self.childrenBlocks = []

    def addLine(self, line):
        self.lines.append(line)
