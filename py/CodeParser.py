from CodeClass import CodeClass
from CodeFunction import CodeFunction
from CodeFile import CodeFile


class CodeParser:
    
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
            self.numLines = len(self.lines)
        self.currentLineNum = 0
        self.currentLine = self.lines[0]

    def nextLine(self):
        self.currentLineNum += 1
        self.currentLine = self.lines[self.currentLineNum]
        return self.currentLine

    def peekLine(self):
        if notEndOfFile:
            return self.lines[currentLineNum + 1]
        return None

    def stepBack(self):
        if self.currentLineNum > 0:
            self.currentLineNum = self.currentLineNum -1
            self.currentLine = self.lines[self.currentLineNum]

    def notEndOfFile(self):
        return self.currentLineNum < self.numLines

    def notLastLine(self):
        return self.currentLineNum < self.numLines - 1

    def parseFile(self):
        codeFile = CodeFile()
        line = self.currentLine 
        while self.notEndOfFile():
            if 'class' in line.split(' '):
                print("****Parsing CodeClass: {}".format(line.rstrip()))
                classLines = self.packageBlock()
                codeFile.classes.append(self.parseClass(classLines))
                self.stepBack()
            elif 'def' in line.split(' '):
                print("****Parsing CodeFunction: {}".format(line.rstrip()))
                functionLines = self.packageBlock()
                codeFile.functions.append(self.parseFunction(functionLines))
                self.stepBack()
            else:
                codeFile.addLine(line)
            if self.notLastLine():
                line = self.nextLine()
            else:
                break
        return codeFile

    def parseClass(self, lines):
        lineNum = 0
        line = lines[lineNum] 
        className = self.parseClassName(line)
        classFunctions = []
        classLines = []
        print("ClassName: {}".format(className))
        while lineNum < len(lines):
            line = line.strip()
            if 'def' in line.split(' '):
                print("Parsing Function: '{}'".format(line.rstrip()))
                funcLines, lineNum = self.packageBlockLines(lines, lineNum)
                line = lines[lineNum]
                print("FUNCLINES: {}".format(funcLines))
                print("LineAfter: {}".format(line.rstrip()))
                func = self.parseFunction(funcLines)
                classFunctions.append(func)
                if lineNum == len(lines)-1:
                    break
            else:
                classLines.append(line)
                if lineNum < len(lines) - 1:
                    lineNum += 1
                    line = lines[lineNum]
                else:
                    break
        print("Done parsing class")
        return CodeClass(className, classFunctions, classLines)

    def parseClassName(self, line):
        line = line.strip()
        nameStart = line.find('class ') + 6
        nameEnd = 0
        if '(' in line:
            nameEnd = line.find('(')
        else:
            nameEnd = line.find(':')
        return line[nameStart: nameEnd]


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

    def packageBlock(self):
        # Keep reading until indentation is less than or equal to where it began
        # Assumes you can't mix tabs or spaces. Is this correct?
        blockLines = []

        line = self.currentLine
        blockLines.append(line)
        beginningIndentation = self.countIndentation(line) 
        
        line = self.nextLine()
        while self.shouldIgnoreLine(line):
            line = self.nextLine()
        indentation = self.countIndentation(line)
        while self.notEndOfFile() and indentation > beginningIndentation:
            if self.shouldIgnoreLine(line):
                if self.notLastLine():
                    line = self.nextLine()
                    indentation = self.countIndentation(line)
                    continue
                else:
                    break
            blockLines.append(line)
            if self.notLastLine():
                line = self.nextLine()
                indentation = self.countIndentation(line) 
            else:
                break
        return blockLines

    def packageBlockLines(self, lines, lineNum):
        blockLines = []

        line = lines[lineNum]
        blockLines.append(line)
        beginningIndentation = self.countIndentation(line) 
        
        lineNum += 1
        line = lines[lineNum]
        while self.shouldIgnoreLine(line):
            lineNum += 1
            if lineNum == len(lines):
                return blockLines, lineNum
            line = lines[lineNum] 
        indentation = self.countIndentation(line)
        while lineNum < len(lines) and indentation > beginningIndentation:
            if self.shouldIgnoreLine(line):
                if lineNum < len(lines) - 1:
                    lineNum += 1
                    line = lines[lineNum]
                    indentation = self.countIndentation(line)
                    continue
                else:
                    break
            blockLines.append(line)
            if lineNum < len(lines) - 1:
                lineNum += 1
                line = lines[lineNum] 
                indentation = self.countIndentation(line) 
            else:
                break
        return blockLines, lineNum
