import re
from enum import Enum

class LineTypes(Enum):
    REGULAR = 1 
    COMMENT = 2 
    STRING = 3 
    MULTILINE_STRING_START = 4 # Begins a multiline string 
    UNENDED = 5                # Logical line does not end with newline. e.g. x = 5 \ 
    UNENDED_SINGLE_QUOTE_STRING = 6 # Logical line does not end because of ' string
    UNENDED_DOUBLE_QUOTE_STRING = 7 # Logical line does not end because of " string
    CONTINUES_SINGLE_QUOTE_STRING = 8
    CONTINUES_DOUBLE_QUOTE_STRING = 9


class CodeLine:

    def __init__(self, line, lineNumber, lineType=LineTypes.REGULAR):
        self.line = line
        self.lineNumber = lineNumber
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
