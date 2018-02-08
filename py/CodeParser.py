import re
from CodeClass import CodeClass
from CodeFunction import CodeFunction
from CodeFile import CodeFile
from CodeBlock import CodeBlock


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
        if self.notLastLine():
            return self.lines[self.currentLineNum + 1]
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
        #TODO: Remove packageBlock() and just use packageBlockLines()?
        codeFile = CodeFile()
        line = self.currentLine 
        while self.notEndOfFile():
            if 'class' == line.split(' ')[0]:
                print("****Parsing CodeClass: {}".format(line.rstrip()))
                classLines = self.packageBlock()
                codeFile.classes.append(self.parseClass(classLines))
                if self.notLastLine():
                    self.stepBack()
            elif 'def' == line.split(' ')[0]:
                print("****Parsing CodeFunction: {}".format(line.rstrip()))
                functionLines = self.packageBlock()
                codeFile.functions.append(self.parseFunction(functionLines))
                if self.notLastLine():
                    self.stepBack()
            else:
                blockLines = self.packageBlock()
                block = self.parseBlock(blockLines)
                codeFile.blocks.append(block)
                if self.notLastLine():
                    self.stepBack()
            if self.notLastLine():
                line = self.nextLine()
            else:
                break
        return codeFile

    def parseBlock(self, lines):
        blockType = self.determineBlockType(lines)
        block = CodeBlock('noType')
        if (blockType == 'def'):
            block = self.parseFunction(lines)
        elif (blockType == 'class'):
            block = self.parseClass()
        elif (blockType == 'if'):
            block = self.parseIfBlock(lines)
        elif (blockType == 'else'):
            block = self.parseElseBlock(lines)
        elif (blockType == 'elif'):
            block = self.parseElifBlock(lines)
        elif (blockType == 'for'):
            block = self.parseForBlock(lines)
        elif (blockType == 'while'):
            block = self.parseWhileBlock(lines)
        elif (blockType == 'try'):
            block = self.parseTryBlock(lines)
        elif (blockType == 'except'):
            block = self.parseExceptBlock(lines)
        else:
            block = self.parseRegularBlock(lines)
        return block

    def determineBlockType(self, lines):
        firstLine = lines[0].strip().split(' ')
        blockType = firstLine[0]
        return blockType

    def parseIfBlock(self, lines):
        block = self.parseRegularBlock(lines, hasCondition=True)
        block.blockType = 'if'
        return block

    def parseElseBlock(self, lines):
        block = self.parseRegularBlock(lines)
        block.blockType = 'else'
        return block

    def parseElifBlock(self, lines):
        block = self.parseRegularBlock(lines, hasCondition=True)
        block.blockType = 'elif'
        return block

    def parseForBlock(self, lines):
        block = self.parseRegularBlock(lines, hasCondition=True)
        block.blockType = 'for'
        return block

    def parseWhileBlock(self, lines):
        block = self.parseRegularBlock(lines, hasCondition=True)
        block.blockType = 'while'
        return block

    def parseTryBlock(self, lines):
        block = self.parseRegularBlock(lines)
        block.blockType = 'try'
        return block

    def parseExceptBlock(self, lines):
        block = self.parseRegularBlock(lines)
        block.blockType = 'except'
        return block

    def parseRegularBlock(self, lines, hasCondition=False):
        print("Parsing Regular Block")
        block = CodeBlock()
        lineNum = 0
        if hasCondition:
            condition, lineNum = self.parseCondition(lines)
            block.condition = condition
        while lineNum < len(lines):
            line = lines[lineNum]
            if lineNum > 0 and self.lineStartsBlock(line):
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines)
                block.addChildBlock(childBlock)
            else:
                block.addLine(line)
                lineNum += 1
        return block

    def parseCondition(self, lines):
        i = 0
        while ':' not in lines[i]:
            i += 1
        firstLine = "".join(lines[0:i+1])
        firstLine = ' '.join(firstLine.split())
        condition = firstLine[firstLine.find(' ')+1: firstLine.find(':')]
        condition = condition.replace('(', '').replace(')', '')
        print("CONDITION: {}".format(condition))
        return condition, i+1


    def parseClass(self, lines):
        #TODO: Add block parsing to make this more general?
        lineNum = 0
        line = lines[lineNum]
        className = self.parseClassName(line)
        classFunctions = []
        classLines = []
        print("ClassName: {}".format(className))
        while lineNum < len(lines):
            line = lines[lineNum]
            line = line.strip()
            if 'def' in line.split(' '):
                print("Parsing Function: '{}'".format(line.rstrip()))
                funcLines, lineNum = self.packageBlockLines(lines, lineNum)
                print("funclines: {}".format(funcLines))
                func = self.parseFunction(funcLines)
                classFunctions.append(func)
            else:
                classLines.append(line)
                if lineNum < len(lines) - 1:
                    lineNum += 1
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
        name = self.parseFunctionName(lines[0])
        arguments = self.parseFunctionArgs(lines)
        function = CodeFunction(name, arguments)
        lineNum = 0
        while lineNum < len(lines):
            print(lineNum)
            line = lines[lineNum]
            if lineNum > 0 and self.lineStartsBlock(line):
                print("Old Linenum: {}".format(lineNum))
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                print("New Linenum: {}".format(lineNum))
                childBlock = self.parseBlock(childBlockLines)
                function.addChildBlock(childBlock)
            else:
                print("adding line: {}".format(line.strip()))
                function.addLine(line)
                lineNum += 1
        return function 

    def parseFunctionName(self, line):
        nameStart = line.find('def ') + 4
        nameEnd = line.find('(')
        return line[nameStart: nameEnd]

    def parseFunctionArgs(self, lines):
        args = []
        i = 0
        while ')' not in lines[i]:
            i += 1
        firstLine = "".join(lines[0:i+1])
        argString = firstLine[firstLine.find('(')+1: firstLine.find(':')-1]
        args = argString.split(',')
        for i in range(len(args)):
            args[i] = args[i].strip()
        return args

    def countIndentation(self, line):
        if line[0].isspace():
            return len(line) - len(line.lstrip(line[0]))
        else:
            return 0

    def shouldIgnoreLine(self, line):
        return line.isspace() or len(line) == 0

    def packageBlock(self, minDifference=1):
        # Keep reading until indentation is less than or equal to where it began
        # Assumes you can't mix tabs or spaces. Is this correct?
        blockLines = []

        line = self.currentLine
        blockLines.append(line)
        beginningIndentation = self.countIndentation(line) 
        
        if self.notLastLine():
            line = self.nextLine()
        while self.shouldIgnoreLine(line):
            line = self.nextLine()
        indentation = self.countIndentation(line)
        while not self.endOfBlock(indentation, beginningIndentation, minDifference, line):
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

    def endOfBlock(self, indentation, beginningIndentation, minDifference, line):
        return not(self.notEndOfFile() and indentation >= beginningIndentation + minDifference)

    def lineStartsBlock(self, line):
        blockWords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except']
        if line:
            firstWord = line.split()[0]
            firstWord = re.sub("[^a-zA-Z]","", firstWord) #Remove non-alphabet characters
            for word in blockWords:
                if firstWord == word:
                    return True
            return False
        return False

    def packageBlockLines(self, lines, lineNum, minDifference=1):
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
        while lineNum < len(lines) and indentation >= beginningIndentation+minDifference:
            if self.shouldIgnoreLine(line):
                if lineNum < len(lines)-1:
                    lineNum += 1
                    line = lines[lineNum]
                    indentation = self.countIndentation(line)
                    continue
                else:
                    break
            blockLines.append(line)
            if lineNum < len(lines)-1:
                lineNum += 1
                line = lines[lineNum] 
                indentation = self.countIndentation(line) 
            else:
                break
        if lineNum == len(lines)-1:
            lineNum += 1
        return blockLines, lineNum

