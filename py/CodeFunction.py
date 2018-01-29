class CodeFunction:

    def __init__(self):
        self.name = ''
        self.arguments = []
        self.codeBlocks = []
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)
