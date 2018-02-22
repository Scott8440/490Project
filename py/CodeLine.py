import re
from enum import Enum

class LineTypes(Enum):
    REGULAR = 1 
    COMMENT = 2 
    BLOCK_START = 3             # Line signifies the beginning of a new block
    STARTS_PARENTHESES_LINE = 4
    CONTINUES_PARENTHESES_LINE = 5
    ENDS_PARENTHESES_LINE = 6
    STARTS_CBRACE_LINE = 7
    CONTINUES_CBRACE_LINE = 8
    ENDS_CBRACE_LINE = 9
    STARTS_SBRACE_LINE = 10
    CONTINUES_SBRACE_LINE = 11
    ENDS_SBRACE_LINE = 12
    STARTS_MULTILINE_STRING = 13 # Begins a multiline string 
    CONTINUES_MULTILINE_STRING = 14 
    ENDS_MULTILINE_STRING = 15
    STARTS_SINGLE_QUOTE_STRING = 16 # Logical line does not end because of ' string
    CONTINUES_SINGLE_QUOTE_STRING = 17
    ENDS_SINGLE_QUOTE_STRING = 18
    STARTS_DOUBLE_QUOTE_STRING = 19 # Logical line does not end because of " string
    CONTINUES_DOUBLE_QUOTE_STRING = 20
    ENDS_DOUBLE_QUOTE_STRING = 21


class CodeLine:

    def __init__(self, line, lineNumber, indentation, lineType=LineTypes.REGULAR):
        self.line = line
        self.lineNumber = lineNumber
        self.indentation = indentation
        self.lineType = lineType 

    def extractVariables(self):
        # A rudimentary method of parsing out variable names in this line. 
        # Relies on the variable being in the form: "variable = value"
        # This is not required in python but it's a decent way of getting
        # most of the variable names out of a line
        variables = []
        if self.lineType == LineTypes.REGULAR:
            newLine = self.removeString()
        elif self.lineType == LineTypes.MULTILINE_STRING_START:
            newLine = self.removeMultilineStart()
        else:
            return []
        matches = re.findall(r"(([a-zA-Z_])\w*)([ \t])*=", newLine)
        variables = [match[0] for match in matches]
        return variables

    def removeString(self):
        # Removes the strings in a single-line line. Multiline strings dealt with in other function
        stringStart = None
        stringChar = None
        stringsLeft = True
        newLine = self.line
        while stringsLeft:
            i = 0
            stringsLeft = False
            while i < len(newLine):
                char = newLine[i]
                if char == '"' or char == "'":
                    # Skips this if it is actually a multiline signifier
                    if newLine[i:i+3] == char*3:
                        i += 3    
                    else:
                        stringChar = char
                        stringStart = i 
                        stringsLeft = True
                        break
                i += 1
            if stringStart is not None:
                index = i+1
                stringEnd = stringStart
                while index < len(newLine) and newLine[index] != stringChar:
                    char = newLine[index]
                    if char == "\\":
                        index += 1
                    index += 1
                stringEnd = index
                newLine = newLine[:stringStart] + newLine[stringEnd+1:]
            else:
                newLine = self.line
        return self.removeMultilineStart(newLine)

    def removeMultilineStart(self, line=None):
        commentStart = None
        commentEnd = None
        quoteChar = None
        if line is None:
            line = self.line
        if ("'''" in line):
            commentStart = line.find("'''")
            quoteChar = "'''"
        elif ('"""' in line):
            commentStart = line.find('"""')
            quoteChar = '"""' 
        if commentStart is not None:
            commentEnd = line[commentStart+1:].find(quoteChar)
            if commentEnd > commentStart:
                commentEnd += commentStart
                line = line[0:commentStart] + line[commentEnd+4:]
            else:
                line = line[:commentStart]
        return line
