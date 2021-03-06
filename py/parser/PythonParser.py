import re
from py.code_rep.CodeClass import CodeClass
from py.code_rep.CodeFunction import CodeFunction
from py.code_rep.CodeFile import CodeFile
from py.code_rep.CodeBlock import CodeBlock
from py.code_rep.CodeLine import CodeLine
from py.code_rep.LineTypes import LineTypes
from py.parser.CodeParser import CodeParser, FileTypeError
import py.code_rep.LineHelpers as LineHelpers


class PythonParser(CodeParser):

    def __init__(self, filename):
        if filename[-3:] != '.py':
            raise FileTypeError
        CodeParser.__init__(self, filename)
        self.currentCodedLineIndex = 0
        self.logicalLines = self.removeEscapeNewlines()
        self.codedLines = self.codifyLines()

    def getCodedLine(self):
        if self.currentCodedLineIndex < len(self.codedLines):
            newLine = self.codedLines[self.currentCodedLineIndex]
            self.currentCodedLineIndex += 1
            return newLine
        else:
            return None

    def consumeLine(self):
        self.currentCodedLineIndex += 1

    def stepBack(self):
        self.currentCodedLineIndex -= 1

    def parseFile(self):
        codeFile = CodeFile(filename=self.filename)
        line = self.getCodedLine()
        while line:
            if self.lineStartsBlock(line):
                codeFile.addChildBlock(self.parseBlock(line))
            else:
                codeFile.addLine(line)
            line = self.getCodedLine()
        return codeFile

    def parseBlock(self, line, parentBlock=None):
        text = line.line
        startLineNumber = line.lineNumber
        baseIndentation = line.indentation
        blockType = self.determineBlockType(text)
        block = CodeBlock(startLineNumber, parentBlock=parentBlock)

        if (blockType == 'def'):
            name = self.parseFunctionName(text)
            args = self.parseFunctionArgs(line)
            block = CodeFunction(name, args, startLineNumber, parentBlock=parentBlock)
        elif (blockType == 'class'):
            name = self.parseClassName(text)
            parentClasses = self.parseFunctionArgs(line)
            block = CodeClass(name, parentClasses, startLineNumber, parentBlock=parentBlock)
        elif (blockType == 'if'):
            condition = self.parseCondition(line, block)
            block.condition = condition
            block.blockType = blockType
        elif (blockType == 'else'):
            block.blockType = blockType
            self.consumeLine()
        elif (blockType == 'elif'):
            condition = self.parseCondition(line, block)
            block.condition = condition
            block.blockType = blockType
        elif (blockType == 'for'):
            condition = self.parseCondition(line, block)
            block.condition = condition
            block.blockType = blockType
        elif (blockType == 'while'):
            condition = self.parseCondition(line, block)
            block.condition = condition
            block.blockType = blockType
        elif (blockType == 'try'):
            block.blockType = blockType
            self.consumeLine()
        elif (blockType == 'except'):
            block.blockType = blockType
            self.consumeLine()
        else:
            block.blockType = 'noType'
            self.consumeLine()
        block = self.buildBlock(baseIndentation, block)
        return block

    def buildBlock(self, baseIndentation, block):
        # starts on the first line after the block definition
        # then continues through the file until the indentation is less than
        # the base indentation. If a new block is defined within this block,
        # it recursively parses the block and adds it as a child

        line = self.getCodedLine()
        while line is not None and (line.indentation is None or line.indentation > baseIndentation):
            if self.lineStartsBlock(line):
                childBlock = self.parseBlock(line, parentBlock=block)
                block.addChildBlock(childBlock)
            else:
                block.addLine(line)
            line = self.getCodedLine()
        if line:
            self.stepBack()
        return block

    def determineBlockType(self, text):
        firstWord = re.findall(r"[\w']+", text.strip().split(' ')[0])[0]
        blockType = re.sub("[^a-zA-Z]", "", firstWord)  # Remove non-alphabet characters
        return blockType

    def getMultilineCommentLength(self, lines, lineIndex):
        start = lineIndex
        end = start
        firstLine = lines[start][0]
        ender = "'''"
        if ('"""' in firstLine):
            ender = '"""'
        if firstLine.count(ender) % 2 == 0:
            return 1
        end += 1
        while end < len(lines) and lines[end][0].count(ender) < 1:
            end += 1
        return end - start + 1

    def parseCondition(self, line, block):
        conLine = line.line.strip()
        block.addLine(line)
        if ':' not in line.stripLine():
            line = self.getCodedLine()
            block.addLine(line)
            while line and ':' not in line.stripLine():
                conLine += " " + line.line.strip()
                line = self.getCodedLine()
                if line and ':' not in line.stripLine():  # TODO: Fix this thing
                    block.addLine(line)
            conLine += " " + line.line.strip()
        conLine = conLine.replace("\n", " ")
        condition = conLine[conLine.find(' ')+1: conLine.find(':')]
        return condition

    def parseClassName(self, text):
        text = text.strip()
        token = 'class '
        nameStart = text.find(token) + len(token)
        nameEnd = 0
        if '(' in text:
            nameEnd = text.find('(')
        else:
            nameEnd = text.find(':')
        return text[nameStart: nameEnd]

    def parseFunctionName(self, text):
        token = 'def '
        nameStart = text.find(token) + len(token)
        nameEnd = text.find('(')
        return text[nameStart: nameEnd]

    def parseFunctionArgs(self, line):
        args = []
        linesConsumed = 0
        argLine = line.line
        if ('(' not in line.line):
            return args, 0
        while ')' not in line.line:
            if linesConsumed > 0:
                argLine += line.line
            line = self.getCodedLine()
            linesConsumed += 1
        if linesConsumed > 0:
            argLine += line.line
        argString = argLine[argLine.find('(')+1: argLine.find(':')-1]
        if len(argString) > 0:
            args = argString.split(',')
            for j in range(len(args)):
                args[j] = args[j].strip()
        return args

    def countIndentation(self, text):
        # See https://docs.python.org/3/reference/lexical_analysis.html
        # section 2.1.8 Indentation for algorithm explanation
        lineSpace = ''
        if text[0].isspace():
            spaceEnd = 0
            while spaceEnd < len(text) and text[spaceEnd].isspace():
                if text[spaceEnd] == '\t':
                    spacesPerTab = 0
                    for i in range(8):
                        if spaceEnd + i % 8 == 0:
                            spacesPerTab = i
                            break
                    text.replace('\t', ' '*spacesPerTab, 1)
                    spaceEnd += spacesPerTab
                else:
                    spaceEnd += 1
            lineSpace = text[:spaceEnd]
        return len(lineSpace)

    def shouldIgnoreLine(self, text):
        return text.isspace() or (len(text) == 0)

    def shouldIgnoreIndentation(self, text):
        return self.shouldIgnoreLine(text) or (text.strip()[0] == '#')

    def lineStartsBlock(self, line):
        # TODO: Abstract out into another class which will help with multi-language parsing?
        # i.e. Have a class that stores the block words, reserved words, etc. for each language
        blockWords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except']
        text = line.stripLine()
        if text:
            wordMatches = re.findall(r"[\w']+", text)
            if not wordMatches:
                return False
            firstWord = wordMatches[0]
            firstWord = re.sub("[^a-zA-Z]", "", firstWord)
            for word in blockWords:
                if firstWord == word:
                    return True
        return False

    def removeEscapeNewlines(self):
        lineNumber = 0
        logicalLines = []
        while lineNumber < self.numLines:
            line = self.lines[lineNumber]
            if self.shouldIgnoreLine(line):
                lineNumber += 1
            elif self.lineIsEscaped(line):
                multilineLength = 0
                logicalLine = ""
                while self.lineIsEscaped(line):
                    logicalLine += line
                    multilineLength += 1
                    line = self.lines[lineNumber+multilineLength]
                logicalLine += line
                multilineLength += 1
                logicalLines.append((logicalLine, lineNumber+1))  # Add 1 to reflect 0-indexing
                lineNumber += multilineLength
            else:
                logicalLines.append((line, lineNumber+1))
                lineNumber += 1
        return logicalLines

    def lineIsEscaped(self, text):
        return text[-2] == '\\'

    # Turn all lines into CodeLine objects. Takes care of all multiline
    # strings/segments by assigning them the correct indentation. These lines
    # can then be parsed into the correct blocks easily
    def codifyLines(self):
        codedLines = []
        lineNumber = 0
        lineIndex = 0
        while lineIndex < len(self.logicalLines):
            text = self.logicalLines[lineIndex][0]
            lineNumber = self.logicalLines[lineIndex][1]
            indentation = self.countIndentation(text)
            multilineToken = self.startsMultilineComment(text)
            # TODO: Handle multiline string and multiline segment at same time
            if multilineToken:
                lineIndex = self.codifyMultilineComment(text, lineIndex, multilineToken, codedLines)
            elif self.startsMultilineSegment(text):
                segmentLength = self.parseMultilines(lineIndex, indentation)
                for i in range(segmentLength):
                    codedLines.append(CodeLine(self.logicalLines[lineIndex+i][0], lineNumber+i, indentation))
                lineIndex += segmentLength
            elif self.shouldIgnoreIndentation(text):
                codedLines.append(CodeLine(text, lineNumber, None))
                lineIndex += 1
            else:
                codedLines.append(CodeLine(text, lineNumber, indentation))
                lineIndex += 1
        return codedLines

    def codifyMultilineComment(self, text, lineIndex, multilineToken, codedLines):
        stringLength = self.getMultilineCommentLength(self.logicalLines, lineIndex)
        startType = None
        endType = None
        if multilineToken == '"""':
            startType = LineTypes.STARTS_DOUBLE_MULTILINE_STRING
            endType = LineTypes.ENDS_DOUBLE_MULTILINE_STRING
        else:
            startType = LineTypes.STARTS_SINGLE_MULTILINE_STRING
            endType = LineTypes.ENDS_SINGLE_MULTILINE_STRING
        lineNumber = self.logicalLines[lineIndex][1]
        indentation = self.countIndentation(text)
        codedLines.append(CodeLine(text, lineNumber, indentation, lineType=startType))
        for i in range(1, stringLength-1):
            codedLines.append(CodeLine(self.logicalLines[lineIndex+i][0],
                              lineNumber+i, indentation,
                              lineType=LineTypes.CONTINUES_MULTILINE_STRING))
        codedLines.append(CodeLine(self.logicalLines[lineIndex+stringLength-1][0],
                                   lineNumber+stringLength-1, indentation,
                                   lineType=endType))
        return lineIndex + stringLength

    def startsMultilineComment(self, text):
        position = None
        token = None
        if ("'''" in text):
            position = text.find("'''")
            otherQuoteChar = '"'
            token = "'''"
        elif ('"""' in text):
            position = text.find('"""')
            otherQuoteChar = "'"
            token = '"""'
        if position is not None:
            leftLine = text[:position]
            if (('#' in leftLine) or (leftLine.count(otherQuoteChar) % 2 == 1)
               or text.count(token) % 2 == 0):
                return False
        return token

    def startsMultilineSegment(self, text):
        tokenMap = {'(': ')', '[': ']', '{': '}'}
        for char in tokenMap.keys():
            if (LineHelpers.countRealCharacter(text, char) >
               LineHelpers.countRealCharacter(text, tokenMap[char])):
                return True
        return False

    # Uses a stack to parse token-by-token
    # indentation is the same as the first indentation for all lines in this group
    # Start parsing here if this line is determined to begin a multiline segment
    def parseMultilines(self, lineIndex, indentation):
        stack = []
        segmentLength = 0
        startTokens = ['\'', '"', '(', '[', '{']
        line = self.logicalLines[lineIndex][0]
        lineLength = len(line)
        index = 0
        while index < lineLength:
            char = line[index]
            index += 1
            activeStarters = startTokens
            endingToken = ''
            if stack:
                endingToken = self.getEndToken(stack[-1])
                if stack[-1] in ['"', '\'']:
                    # in string mode, nothing can be added to stack
                    activeStarters = []
            if char in activeStarters:
                stack.append(char)
            elif char == endingToken:
                stack.pop()
            elif char == '\n':
                segmentLength += 1
                if stack == []:
                    break
                else:  # Start parsing next line
                    lineIndex += 1
                    line = self.logicalLines[lineIndex][0]
                    lineLength = len(line)
                    index = 0
        return segmentLength

    def getEndToken(self, token):
        return {'\'': '\'', '"': '"', '(': ')', '[': ']', '{': '}'}[token]
