from py.parser.CodeFunction import CodeFunction
from py.parser.CodeClass import CodeClass


class CodeFile:

    def __init__(self, filename=''):
        self.filename = filename 
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
