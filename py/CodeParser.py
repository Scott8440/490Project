import re
from py.CodeClass import CodeClass
from py.CodeFunction import CodeFunction
from py.CodeFile import CodeFile
from py.CodeBlock import CodeBlock
from py.CodeLine import CodeLine, LineTypes

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
            block = self.parseBlock(blockLines, fileLineNumber)
            if isinstance(block, CodeFunction):
                codeFile.functions.append(block)
            elif isinstance(block, CodeClass):
                codeFile.classes.append(block)
            else:
                codeFile.blocks.append(block)
        return codeFile

    def parseBlock(self, lines, startLineNumber):
        blockType = self.determineBlockType(lines)
        block = None
        if (blockType == 'def'):
            block = self.parseFunction(lines, startLineNumber)
        elif (blockType == 'class'):
            block = self.parseClass(lines, startLineNumber)
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
            block.blockType = 'noType'
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
        #TODO: Get rid of 'skipFirstLine' and just pass in lines[1:] from those functions
        block = CodeBlock(startLineNumber)
        lineNum = 0
        if hasCondition:
            condition, lineNum = self.parseCondition(lines)
            block.condition = condition
        elif skipFirstLine:
            lineNum += 1
        while lineNum < len(lines):
            line = lines[lineNum]
            fileLineNumber = startLineNumber + lineNum
            #TODO: strip comments, add comments to object, maybe?
            if self.shouldIgnoreLine(line):
                lineNum += 1
            elif self.startsMultilineComment(line):
                #TODO: Find a way to record that the first line is a real line, and the following lines are STRINGS
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    block.addLine(CodeLine(line, fileLineNumber, CodeLine.lineType.STRING))
                    lineNum += 1
            elif lineNum > 0 and self.lineStartsBlock(line):
                childBlockLines, lineNum = self.packageBlockLines(lines, lineNum)
                childBlock = self.parseBlock(childBlockLines, fileLineNumber)
                block.addChildBlock(childBlock)
            else:
                block.addLine(CodeLine(line, fileLineNumber))
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
            if (('#' in leftLine) or (leftLine.count(otherQuoteChar) % 2 == 1)):
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
        lineNum = 0
        numLines = len(lines)
        className = self.parseClassName(lines[lineNum])
        classParents, lineNum = self.parseFunctionArgs(lines)
        classFunctions = []
        classLines = []
        while lineNum < numLines:
            line = lines[lineNum].strip()
            if self.shouldIgnoreLine(line):
                lineNum += 1
            elif self.startsMultilineComment(line):
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
        return CodeClass(className, classFunctions, classParents, classLines, startLineNumber)

    def parseClassName(self, line):
        line = line.strip()
        nameStart = line.find('class ') + 6 #TODO: Remove magic number
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
            elif self.startsMultilineComment(line):
                commentLength = self.getMultilineCommentLength(lines, lineNum)
                for i in range(commentLength):
                    function.addLine(CodeLine(lines[lineNum], startLineNumber+lineNum, CodeLine.lineType.STRING))
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
        nameStart = line.find('def ') + 4 #TODO: Get rid of this magic number
        nameEnd = line.find('(')
        return line[nameStart: nameEnd]

    def parseFunctionArgs(self, lines): #TODO: Rename since it can be used for more than one thing
        args = []
        i = 0
        if ('(' not in lines[0]):
            return args, 0
        while ')' not in lines[i]:
            i += 1
        firstLine = "".join(lines[0:i+1])
        argString = firstLine[firstLine.find('(')+1: firstLine.find(':')-1]
        if len(argString) > 0: 
            args = argString.split(',')
            for j in range(len(args)):
                args[j] = args[j].strip()
        return args, i+1

    def countIndentation(self, line):
        lineSpace = ''
        if line[0].isspace():
            spaceEnd = 0
            while spaceEnd < len(line) and line[spaceEnd].isspace():
                spaceEnd += 1
            lineSpace = line[:spaceEnd].replace('\t', '    ') #TODO: Will this work if the tablength isn't 4?
        return len(lineSpace)

    def shouldIgnoreLine(self, line):
        return line.isspace() or len(line) == 0

    def shouldIgnoreIndentation(self, line):
        return self.shouldIgnoreLine(line) or line.strip()[0] == '#' 

    def lineStartsBlock(self, line):
        #TODO: Abstract out into another class which will help with multi-language parsing?
        # i.e. Have a class that stores the block words, reserved words, etc. for each language
        blockWords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except']
        if line:
            firstWord = re.findall(r"[\w']+", line)[0]
            firstWord = re.sub("[^a-zA-Z]","", firstWord)
            for word in blockWords:
                if firstWord == word:
                    return True
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
        while (lineNum < numLines and
               ((self.countIndentation(lines[lineNum]) >= beginningIndentation+minDifference) or
               (self.shouldIgnoreIndentation(lines[lineNum])))):
            blockLines.append(lines[lineNum])
            if lineNum < numLines:
                lineNum += 1
        return blockLines, lineNum

    def removeEscapeNewlines(self):
        lineNumber = 0
        logicalLines = []
        while lineNumber < self.numLines:
            line = self.lines[lineNumber]
            if self.lineIsEscaped(line):
                multilineLength = 0
                logicalLine = "" 
                while self.lineIsEscaped(line):
                    logicalLine += line    
                    multilineLength +=1 
                    line = self.lines[lineNumber+multilineLength]
                logicalLine += line
                multilineLength += 1
                logicalLines.append((logicalLine, lineNumber+1))
                lineNumber += multilineLength
            else:
                logicalLines.append((line, lineNumber+1))
                lineNumber += 1
        return logicalLines

    def lineIsEscaped(self, line):
        return line[-2] == '\\'


    # Turn all lines into CodeLine objects
    def codifyLines(self):
        codedLines = []

        prevLineType = LineTypes.REGULAR
        prevIndentation = 0
        lineNumber = 0
        while lineNumber < self.numLines:
            text = self.lines[lineNumber]
            lineType = self.determineLineType(text, prevLineType)
            indentation = self.calculateIndentation(text, lineType, prevIndentation)
            codedLines.append(CodeLine(text, lineNumber, indentation, lineType=lineType))

    # Uses a stack to parse token-by-token
    # indentation is the same as the first indentation for all lines in this group
    # Start parsing here if this line is determined to begin a multiline segment
    def parseMultilines(self, lineNumber, indentation, lineType):
        print(" **** PARSING NEW MULTILINE SEGMENT **** ")
        stack = []
        codedLines = []
        # Must be in regular mode as the line starts, so first token is a real one
        startTokens = ['\'', '"', '(', '[', '{']
        endTokens = [')', ']', '}']
        line = self.lines[lineNumber]
        lineLength = len(line)
        # Modes are either REGULAR, Single_quote_string, double_quote_string, multiline_single, multiline_double
        prevLineType = LineTypes.REGULAR 
        index = 0
        print("Line: {}".format(line.rstrip()))
        while index < lineLength:
            char = line[index]
            index += 1
            stringMode = False
            activeStarters = startTokens
            endingToken = ''
            if stack:
                endingToken = self.getEndToken(stack[-1])
                if stack[-1] in ['"', '\'']: # in string mode, nothing can be added to stack
                    activeStarters = []
            if char in activeStarters:
                print("Appended {}".format(char))
                stack.append(char)
            elif char == endingToken:
                print("Popped")
                stack.pop()
            elif char == '\n':
                print("Found newline")
                # line ends with a certain type
                lineType = self.getLineTypeFromStack(stack, prevLineType)
                codedLines.append(CodeLine(line, lineNumber, indentation, lineType=lineType))
                if stack == []:
                    print("Stack empty on newline")
                    break
                else:
                    print("Stack not empty on newline: {}".format(stack))
                    # Start parsing next line
                    prevLineType = lineType
                    lineNumber += 1
                    line = self.lines[lineNumber]
                    print("new Line: {}".format(line.rstrip()))
                    lineLength = len(line)
                    index =0
        return codedLines

    def getEndToken(self, token):
        tokenMap = {'\'': '\'', '"': '"', '(': ')', '[': ']', '{': '}'}
        return tokenMap[token]

    def getLineTypeFromStack(self, stack, prevLineType):
        print("Prev Type: {}".format(prevLineType))
        tokenMap = {}
        if len(stack) == 0:
            if prevLineType == LineTypes.STARTS_CBRACE_LINE:
                return LineTypes.ENDS_CBRACE_LINE
            elif prevLineType == LineTypes.STARTS_SBRACE_LINE:
                return LineTypes.ENDS_SBRACE_LINE
            elif prevLineType == LineTypes.STARTS_PARENTHESES_LINE:
                return LineTypes.ENDS_PARENTHESES_LINE
            elif prevLineType == LineTypes.STARTS_SINGLE_QUOTE_STRING:
                return LineTypes.ENDS_SINGLE_QUOTE_STRING
            elif prevLineType == LineTypes.STARTS_DOUBLE_QUOTE_STRING:
                return LineTypes.ENDS_DOUBLE_QUOTE_STRING
            elif prevLineType == LineTypes.REGULAR:
                return LineTypes.REGULAR
            return prevLineType 
        else:
            token = stack[-1]
            if prevLineType == LineTypes.REGULAR:
                tokenMap = {'\'': LineTypes.STARTS_SINGLE_QUOTE_STRING,
                            '"' : LineTypes.STARTS_DOUBLE_QUOTE_STRING,
                            '(' : LineTypes.STARTS_PARENTHESES_LINE,
                            '[' : LineTypes.STARTS_SBRACE_LINE,
                            '{' : LineTypes.STARTS_CBRACE_LINE}
            else:
                tokenMap = {'\'': LineTypes.CONTINUES_CBRACE_LINE,
                            '"' : LineTypes.CONTINUES_DOUBLE_QUOTE_STRING,
                            '(' : LineTypes.CONTINUES_PARENTHESES_LINE,
                            '[' : LineTypes.CONTINUES_SBRACE_LINE,
                            '{' : LineTypes.CONTINUES_CBRACE_LINE}
            return tokenMap[token]
