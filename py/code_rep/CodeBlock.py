from py.code_rep.Variable import Variable


class CodeBlock:

    def __init__(self, lineNumber, parentBlock=None, blockType=None):
        self.blockType = blockType
        # self.variables = {} # Map variable name to line it was defined on
        self.variables = []
        self.lines = []
        self.childrenBlocks = []
        self.condition = None
        self.lineNumber = lineNumber
        self.parentBlock = parentBlock

    def setType(self, blockType):
        self.blockType = blockType

    def addLine(self, line):
        self.lines.append(line)
        for var_name in line.extractVariables(): # Add variables as lines are added
            if self._shouldAddVariable(var_name):
                self.variables.append(Variable(var_name, line.lineNumber))

    def _shouldAddVariable(self, var_name):
        variable_names = [var.name for var in self.variables]
        if var_name in variable_names:
            return False
        if self.parentBlock:
            parent_var_names = [var.name for var in self.parentBlock.variables]
            return var_name not in parent_var_names
        return True

    def addChildBlock(self, block):
        self.childrenBlocks.append(block)

    def getLength(self):
        length = len(self.lines)
        for block in self.childrenBlocks:
            length += block.getLength()
        return length

    def getAllVariables(self):
        allVars = self.variables
        for block in self.childrenBlocks:
            allVars.extend(block.getAllVariables())
        return allVars

    def getAllLines(self):
        lines = self.lines
        for block in self.childrenBlocks:
            lines += block.getAllLines()
        return lines

    def printSelf(self, level=1):
        indent = "  "*level
        print("{}{}<{} Block>: {}".format(self.lineNumber, indent, self.blockType, self.getLength()))
        if self.condition:
            print("{}    Condition: {}".format(indent, self.condition))
        print("{}    Block Vars: {}".format(indent, self.variables))
        if self.lines:
            for j in self.lines:
                print("{}  {}{}".format(j.lineNumber, indent, j.line.strip()))
        for j in self.childrenBlocks:
            j.printSelf(level=level+1)
