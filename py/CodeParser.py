from CodeClass import CodeClass
from CodeFunction import CodeFunction


class CodeParser:

    def __init__(self):
        pass

    def parseClass(self, lines):
        print("Class Length: {}".format(len(lines)))
        newClass = CodeClass()
        lineNum = 0
        line = lines[lineNum]
        print(lines)
        while lineNum < len(lines):
            line = line.strip()
            #print(line)
            if 'def' in line.split(' '):
                print("Parsing Function: '{}'".format(line.rstrip()))
                funcLines = self.packageBlock(lines, lineNum)
                lineNum += len(funcLines)
                func = self.parseFunction(funcLines)
                newClass.addFunction(func)
            else:
                newClass.addLine(line)
                lineNum += 1
                line = lines[lineNum]
        return newClass

    def parseFunction(self, lines):
        print("Function Length: {}".format(len(lines)))
        newFunction = CodeFunction()
        for line in lines:
            newFunction.addLine(line)
        return newFunction

    def countIndentation(self, line):
        #print("First Character: '{}'".format(line[0]))
        if line[0].isspace():
            return len(line) - len(line.lstrip(line[0]))
        else:
            return 0

    def shouldIgnoreLine(self, line):
        return line.isspace() or len(line) == 0

    def packageBlock(self, lines, lineNumber):
        # Keep reading until indentation is less than or equal to where it began
        # Assumes you can't mix tabs or spaces. Is this correct?
        blockLines = []

        line = lines[lineNumber]
        beginningIndentation = self.countIndentation(line) 
        
        lineNumber += 1
        line = lines[lineNumber]
        while self.shouldIgnoreLine(line):
            #print("ignored line")
            lineNumber += 1
            line = lines[lineNumber] 
        indentation = self.countIndentation(line)
        #print("First indent: {}".format(beginningIndentation))
        #print("first line: '{}'".format(line.rstrip()))
        #print("indent: {}".format(indentation))
        while line and indentation > beginningIndentation:
            if self.shouldIgnoreLine(line):
                lineNumber += 1
                line = lines[lineNumber]
                indentation = self.countIndentation(line)
                continue

            blockLines.append(line)
            lineNumber += 1
            line = lines[lineNumber]
            indentation = self.countIndentation(line) 
            #print("indent: {}".format(indentation))
        return blockLines, lineNumber
