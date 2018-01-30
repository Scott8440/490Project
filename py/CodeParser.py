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
            elif 'def' in line.split(' '):
                print("****Parsing CodeFunction: {}".format(line.rstrip()))
                functionLines = self.packageBlock()
                codeFile.functions.append(self.parseFunction(functionLines))
            else:
                codeFile.addLine(line)
            if self.notLastLine():
                line = self.nextLine()
            else:
                break
        return codeFile

    def parseClass(self):
        print("Class Length: {}".format(len(lines)))
        newClass = CodeClass()
        line = self.currentLine
        while self.notEndOfFile():
            line = line.strip()
            if 'def' in line.split(' '):
                print("Parsing Function: '{}'".format(line.rstrip()))
                funcLines = self.packageBlock()
                print("FUNCLINES: {}".format(funcLines))
                func = self.parseFunction(funcLines)
                newClass.addFunction(func)
            else:
                newClass.addLine(line)
                if self.notLastLine():
                    line = self.nextLine()
                else:
                    break
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

    def packageBlock(self):
        # Keep reading until indentation is less than or equal to where it began
        # Assumes you can't mix tabs or spaces. Is this correct?
        blockLines = []

        #line = lines[lineNumber]
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
