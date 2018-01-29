from CodeClass import CodeClass
from CodeFunction import CodeFunction


class CodeParser:

    def __init__(self):
        pass

    def parseClass(self, lines):
        print("Class Length: {}".format(len(lines)))
        newClass = CodeClass()
        for line in lines:
            newClass.addLine(line)
        return newClass

    def parseFunction(self, lines):
        print("Function Length: {}".format(len(lines)))
        newFunction = CodeFunction()
        for line in lines:
            newFunction.addLine(line)
        return newFunction

    def countIndentation(self, line):
        if line[0].isspace():
            return len(line) - len(line.lstrip(line[0]))
        else:
            return 0

    def packageBlock(self, filePointer, firstLine):
        # Keep reading until indentation is less than or equal to where it began
        # Assumes you can't mix tabs or spaces. Is this correct?
        blockLines = []
        
        line = filePointer.readline()
        beginningIndentation = self.countIndentation(firstLine) 
        print("First indent: {}".format(beginningIndentation))
        indentation = self.countIndentation(line)
        print("indent: {}".format(indentation))
        while line and indentation > beginningIndentation:
            line = filePointer.readline()
            if line.isspace() or len(line) == 0:
                continue
            blockLines.append(line)
            indentation = self.countIndentation(firstLine) 
            print("indent: {}".format(indentation))
        return blockLines
