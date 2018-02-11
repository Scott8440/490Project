import re
from CodeClass import CodeClass
from CodeFunction import CodeFunction
from CodeFile import CodeFile
from CodeBlock import CodeBlock
from CodeLine import CodeLine

class CodeParser:
    
    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
            self.numLines = len(self.lines)

    def notEndOfFile(self, lineNum):
        return lineNum < self.numLines

    def notLastLine(self, lineNum):
        return lineNum < self.numLines - 1

    def parseFile(self):
        codeFile = CodeFile()
        lineNum = 0
        while self.notEndOfFile(lineNum):
            line = self.lines[lineNum] 
            fileLineNumber = lineNum+1 #because the list is 0-indexed
            blockLines, lineNum = self.packageBlockLines(self.lines, lineNum)
            # TODO: Remove the switch cases here since they already exist in parseBlock()
            if 'class' == line.split(' ')[0]:
                codeFile.classes.append(self.parseClass(blockLines, fileLineNumber))
            elif 'def' == line.split(' ')[0]:
                print("Function def at line: {}".format(lineNum))
                codeFile.functions.append(self.parseFunction(blockLines, fileLineNumber))
            else:
                block = self.parseBlock(blockLines, fileLineNumber)
                codeFile.blocks.append(block)
        return codeFile

    def parseBlock(self, lines, startLineNumber):
        blockType = self.determineBlockType(lines)
        block = CodeBlock(startLineNumber, blockType='noType')
        if (blockType == 'def'):
            block = self.parseFunction(lines, startLineNumber)
        elif (blockType == 'class'):
            block = self.parseClass()
        elif (blockType == 'if'):
            block = self.parseIfBlock(lines, startLineNumber)
        elif (blockType == 'else'):
            block = self.parseElseBlock(lines, startLineNumber)
        elif (blockType == 'elif'):
            block = self.parseElifBlock(lines, startLineNumber)
        elif (blockType == 'for'):
            block = self.parseForBlock(lines, startLineNumber)
        elif (blockType == 'while'):
            block = self.parseWhileBlock(lines, startLineNumber)
        elif (blockType == 'try'):
            block = self.parseTryBlock(lines, startLineNumber)
        elif (blockType == 'except'):
            block = self.parseExceptBlock(lines, startLineNumber)
        else:
            block = self.parseRegularBlock(lines, startLineNumber)
        return block

    def determineBlockType(self, lines):
        firstLine = re.findall(r"[\w']+", lines[0])
        blockType = re.sub("[^a-zA-Z]","", firstLine[0]) #Remove non-alphabet characters
        return blockType

    def parseIfBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, hasCondition=True)
        block.blockType = 'if'
        return block

    def parseElseBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, skipFirstLine=True)
        block.blockType = 'else'
        return block

    def parseElifBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, hasCondition=True)
        block.blockType = 'elif'
        return block

    def parseForBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, hasCondition=True)
        block.blockType = 'for'
        return block

    def parseWhileBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, hasCondition=True)
        block.blockType = 'while'
        return block

    def parseTryBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, skipFirstLine=True)
        block.blockType = 'try'
        return block

    def parseExceptBlock(self, lines, startLineNumber):
        block = self.parseRegularBlock(lines, startLineNumber, skipFirstLine=True)
        block.blockType = 'except'
        return block

    def parseRegularBlock(self, lines, startLineNumber, hasCondition=False, skipFirstLine=False):
        block = CodeBlock(startLineNumber)
        lineNum = 0
        if hasCondition:
            condition, lineNum = self.parseCondition(lines)
            block.condition = condition
        elif skipFirstLine:
            lineNum += 1
        while lineNum < len(lines):
            line = lines[lineNum]
            #TODO: strip comments, add comments to object, maybe?
            if self.shouldIgnoreLine(line):
                lineNum += 1
            elif self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    block.addLine(CodeLine(line, startLineNumber+lineNum))
                    lineNum += 1
            elif lineNum > 0 and self.lineStartsBlock(line):
                blockLineNumber = startLineNumber + lineNum
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines, blockLineNumber)
                block.addChildBlock(childBlock)
            else:
                block.addLine(CodeLine(line, startLineNumber+lineNum))
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
        endLine = 0
        while ':' not in lines[endLine]:
            endLine += 1
        firstLine = "".join(lines[0:endLine+1])
        firstLine = ' '.join(firstLine.split())
        condition = firstLine[firstLine.find(' ')+1: firstLine.find(':')]
        condition = condition.replace('(', '').replace(')', '')
        return condition, endLine+1

    def parseClass(self, lines, startLineNumber):
        #TODO: Add block parsing to make this more general?
        #TODO: Get the class parents
        lineNum = 0
        numLines = len(lines)
        line = lines[lineNum]
        className = self.parseClassName(line)
        classFunctions = []
        classLines = []
        while lineNum < numLines:
            line = lines[lineNum]
            line = line.strip()
            if self.shouldIgnoreLine(line):
                lineNum += 1
                continue
            if self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    classLines.append(CodeLine(line, startLineNumber+lineNum))
                    lineNum += 1
            elif 'def' in line.split(' '):
                funcLines, lineNum = self.packageBlockLines(lines, lineNum)
                func = self.parseFunction(funcLines, startLineNumber+lineNum)
                classFunctions.append(func)
            else:
                classLines.append(CodeLine(line, startLineNumber+lineNum))
                if lineNum < numLines:
                    lineNum += 1
        return CodeClass(className, classFunctions, classLines, startLineNumber)

    def parseClassName(self, line):
        line = line.strip()
        nameStart = line.find('class ') + 6
        nameEnd = 0
        if '(' in line:
            nameEnd = line.find('(')
        else:
            nameEnd = line.find(':')
        return line[nameStart: nameEnd]

    def parseFunction(self, lines, startLineNumber):
        lineNum = 0
        name = self.parseFunctionName(lines[0])
        arguments, lineNum = self.parseFunctionArgs(lines)
        function = CodeFunction(name, arguments, startLineNumber)
        while lineNum < len(lines):
            line = lines[lineNum]
            if self.shouldIgnoreLine(line):
                lineNum += 1
                continue
            if self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    function.addLine(CodeLine(lines[lineNum], startLineNumber+lineNum))
                    lineNum += 1
            elif lineNum > 0 and self.lineStartsBlock(line):
                blockLineNumber = startLineNumber + lineNum
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines, blockLineNumber)
                function.addChildBlock(childBlock)
            else:
                function.addLine(CodeLine(lines[lineNum], startLineNumber+lineNum))
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
            while spaceEnd < len(line) and line[spaceEnd].isspace():
                spaceEnd += 1
            lineSpace = line[:spaceEnd].replace('\t', '    ')
            return len(lineSpace)
        else:
            return 0

    def shouldIgnoreLine(self, line):
        return line.isspace() or len(line) == 0

    def shouldIgnoreIndentation(self, line):
        return self.shouldIgnoreLine(line) or line.strip()[0] == '#' 

    def lineStartsBlock(self, line):
        blockWords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except']
        if line:
            firstWord = re.findall(r"[\w']+", line)[0]
            firstWord = re.sub("[^a-zA-Z]","", firstWord) #Remove non-alphabet characters TODO: is this redundant now?
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

        while self.shouldIgnoreLine(lines[lineNum]):
            lineNum += 1
            if lineNum == numLines:
                return blockLines, lineNum
        while ((lineNum < numLines and 
               self.countIndentation(lines[lineNum]) >= beginningIndentation+minDifference)
               or (lineNum < numLines and self.shouldIgnoreIndentation(lines[lineNum]))):
            line = lines[lineNum]
            blockLines.append(line)
            if lineNum < numLines:
                lineNum += 1
        return blockLines, lineNum

