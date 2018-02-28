from py.CodeFunction import CodeFunction
from py.CodeClass import CodeClass


class CodeFile:

    def __init__(self):
        self.filename = ''
        self.functions = []
        self.classes = []
        self.blocks = []
        self.lines = []

    def addChildBlock(self, block):
        if isinstance(block, CodeFunction):
            self.functions.append(block)
        elif isinstance(block, CodeClass):
            self.classes.append(block)
        else:
            self.blocks.append(block)

    def addLine(self, line):
        self.lines.append(line)
