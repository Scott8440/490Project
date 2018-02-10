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

    def notEndOfFile(self, lineNum):
        return lineNum < self.numLines

    def notLastLine(self, lineNum):
        return lineNum < self.numLines - 1

    def parseFile(self):
        codeFile = CodeFile()
        lineNum = 0
        while self.notEndOfFile(lineNum):
            line = self.lines[lineNum] 
            if 'class' == line.split(' ')[0]:
                classLines, lineNum = self.packageBlockLines(self.lines, lineNum)
                codeFile.classes.append(self.parseClass(classLines))
                if self.notLastLine(lineNum):
                    lineNum -= 1
            elif 'def' == line.split(' ')[0]:
                functionLines, lineNum = self.packageBlockLines(self.lines, lineNum)
                codeFile.functions.append(self.parseFunction(functionLines))
                if self.notLastLine(lineNum):
                    lineNum -= 1
            else:
                blockLines, lineNum = self.packageBlockLines(self.lines, lineNum)
                block = self.parseBlock(blockLines)
                codeFile.blocks.append(block)
                if self.notLastLine(lineNum):
                    lineNum -= 1
            if self.notLastLine(lineNum):
                lineNum += 1
                line = self.lines[lineNum]
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
        firstLine = re.findall(r"[\w']+", lines[0])
        blockType = re.sub("[^a-zA-Z]","", firstLine[0]) #Remove non-alphabet characters
        return blockType

    def parseIfBlock(self, lines):
        block = self.parseRegularBlock(lines, hasCondition=True)
        block.blockType = 'if'
        return block

    def parseElseBlock(self, lines):
        block = self.parseRegularBlock(lines, skipFirstLine=True)
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
        block = self.parseRegularBlock(lines, skipFirstLine=True)
        block.blockType = 'try'
        return block

    def parseExceptBlock(self, lines):
        block = self.parseRegularBlock(lines, skipFirstLine=True)
        block.blockType = 'except'
        return block

    def parseRegularBlock(self, lines, hasCondition=False, skipFirstLine=False):
        block = CodeBlock()
        lineNum = 0
        if hasCondition:
            condition, lineNum = self.parseCondition(lines)
            block.condition = condition
        elif skipFirstLine:
            lineNum += 1
        while lineNum < len(lines):
            line = lines[lineNum]
            #TODO: strip comments, add comments to object
            if self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    block.addLine(lines[lineNum])
                    lineNum += 1
            elif lineNum > 0 and self.lineStartsBlock(line):
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines)
                block.addChildBlock(childBlock)
            else:
                block.addLine(line)
                lineNum += 1
        return block

    def startsMultilineComment(self, line):
        position = None
        quoteChar = None
        if ("'''" in line):
            position = line.find("'''")
            otherQuoteChar = '"'
        elif ('"""' in line):
            position = line.find('"""')
            otherQuoteChar = "'"
        if position is not None:
            leftLine = line[:position]
            if '#' in leftLine:
                return False
            if leftLine.count(otherQuoteChar) % 2 == 1:
                return False
            return True
    
    def getMultilineCommentLength(self, lines, lineNum):
        start = lineNum
        end = start
        firstLine = lines[start]
        ender = "'''"
        if ('"""' in firstLine):
            ender = '"""'
        if firstLine.count(ender) % 2 == 0:
            return 1
        end += 1
        while end < len(lines) and lines[end].count(ender) < 1:
            end += 1
        return end - start + 1

    def parseCondition(self, lines):
        i = 0
        while ':' not in lines[i]:
            i += 1
        firstLine = "".join(lines[0:i+1])
        firstLine = ' '.join(firstLine.split())
        condition = firstLine[firstLine.find(' ')+1: firstLine.find(':')]
        condition = condition.replace('(', '').replace(')', '')
        return condition, i+1


    def parseClass(self, lines):
        #TODO: Add block parsing to make this more general?
        lineNum = 0
        numLines = len(lines)
        line = lines[lineNum]
        className = self.parseClassName(line)
        classFunctions = []
        classLines = []
        while lineNum < numLines:
            line = lines[lineNum]
            line = line.strip()
            if self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    classLines.append(lines[lineNum])
                    lineNum += 1
            elif 'def' in line.split(' '):
                funcLines, lineNum = self.packageBlockLines(lines, lineNum)
                func = self.parseFunction(funcLines)
                classFunctions.append(func)
            else:
                classLines.append(line)
                if lineNum < numLines:
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
        lineNum = 0
        name = self.parseFunctionName(lines[0])
        arguments, lineNum = self.parseFunctionArgs(lines)
        function = CodeFunction(name, arguments)
        while lineNum < len(lines):
            line = lines[lineNum]
            if self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    function.addLine(lines[lineNum])
                    lineNum += 1
            elif lineNum > 0 and self.lineStartsBlock(line):
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines)
                function.addChildBlock(childBlock)
            else:
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
        for j in range(len(args)):
            args[j] = args[j].strip()
        return args, i+1

    def countIndentation(self, line):
        if line[0].isspace():
            spaceEnd = 0
            for i in range(len(line)):
                if not line[i].isspace():
                    spaceEnd = i
                    break
            lineSpace = line[:spaceEnd].replace('\t', '    ')
            return len(lineSpace)
        else:
            return 0

    def shouldIgnoreLine(self, line):
        #TODO: Ignore indentation with comment, but don't ignore comment
        return line.isspace() or len(line) == 0

    def shouldIgnoreIndentation(self, line):
        return self.shouldIgnoreLine(line) or line.strip()[0] == '#' 

    def lineStartsBlock(self, line):
        blockWords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except']
        if line:
            firstWord = re.findall(r"[\w']+", line)[0]
            firstWord = re.sub("[^a-zA-Z]","", firstWord) #Remove non-alphabet characters
            for word in blockWords:
                if firstWord == word:
                    return True
            return False
        return False

    def packageBlockLines(self, lines, lineNum, minDifference=1):
        blockLines = [lines[lineNum]]
        numLines = len(lines)
        beginningIndentation = self.countIndentation(lines[lineNum]) 

        lineNum += 1
        line = lines[lineNum]
        while self.shouldIgnoreLine(line):
            lineNum += 1
            if lineNum == numLines:
                return blockLines, lineNum
            line = lines[lineNum] 
        while ((lineNum < numLines and 
               self.countIndentation(lines[lineNum]) >= beginningIndentation+minDifference)
               or self.shouldIgnoreIndentation(lines[lineNum])):
            line = lines[lineNum]
            if self.shouldIgnoreLine(line):
                if lineNum < numLines-1:
                    lineNum += 1
                    continue
                else:
                    break
            blockLines.append(line)
            if lineNum < numLines-1:
                lineNum += 1
            else:
                break
        if lineNum == numLines-1:
            lineNum += 1
        return blockLines, lineNum

