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
        while lineNum < len(lines):
            line = line.strip()
            if 'def' in line.split(' '):
                print("Parsing Function: '{}'".format(line.rstrip()))
                funcLines, funcLength = self.packageBlock(lines, lineNum)
                print("FUNCLINES: {}".format(funcLines))
                lineNum += funcLength
                func = self.parseFunction(funcLines)
                newClass.addFunction(func)
            else:
                newClass.addLine(line)
                lineNum += 1
                line = lines[lineNum]
        return newClass

    def parseFunction(self, lines):
        firstLine = lines[0]
        name = self.parseFunctionName(firstLine)
        arguments = self.parseFunctionArgs(firstLine)
        #print("Name: {}".format(name))
        #print("Args: {}".format(arguments))
        return CodeFunction(name, arguments, lines)

    def parseFunctionName(self, line):
        nameStart = line.find('def ') + 4
        nameEnd = line.find('(')
        return line[nameStart: nameEnd]

    def parseFunctionArgs(self, line):
        argString = line[line.find('(')+1: line.find(':')-1]
        args = argString.split(',')
        return args

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
        blockLines.append(line)
        beginningIndentation = self.countIndentation(line) 
        
        lineNumber += 1
        line = lines[lineNumber]
        while self.shouldIgnoreLine(line):
            lineNumber += 1
            line = lines[lineNumber] 
        indentation = self.countIndentation(line)
        while lineNumber < len(lines) and indentation > beginningIndentation:
            if self.shouldIgnoreLine(line):
                lineNumber += 1
                if lineNumber == len(lines):
                    break
                line = lines[lineNumber]
                indentation = self.countIndentation(line)
                continue
            blockLines.append(line)
            lineNumber += 1
            if lineNumber == len(lines):
                break
            line = lines[lineNumber]
            indentation = self.countIndentation(line) 
        return blockLines, lineNumber
