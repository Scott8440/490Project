import re
import py.LineHelpers as LineHelpers
from py.LineTypes import LineTypes


class CodeLine:

    def __init__(self, line, lineNumber, indentation, lineType=LineTypes.REGULAR):
        self.line = line
        self.lineNumber = lineNumber
        self.indentation = indentation
        self.lineType = lineType 

    def printLine(self):
        print("('{}',{},{},{})".format(self.line.strip(), self.lineNumber, self.indentation, self.lineType))

    def extractVariables(self):
        # A rudimentary method of parsing out variable names in this line. 
        # Relies on the variable being in the form: "variable = value"
        # This is not required in python but it's a decent way of getting
        # most of the variable names out of a line
        variables = []
        if self.lineType == LineTypes.REGULAR:
            newLine = self.removeStrings()
        elif (self.lineType == LineTypes.STARTS_SINGLE_MULTILINE_STRING 
              or self.lineType == LineTypes.STARTS_DOUBLE_MULTILINE_STRING
              or self.lineType == LineTypes.ENDS_SINGLE_MULTILINE_STRING
              or self.lineType == LineTypes.ENDS_DOUBLE_MULTILINE_STRING):
            newLine = self.removeMultilineString()
        else:
            return []
        matches = re.findall(r"(([a-zA-Z_])\w*)([ \t])*=", newLine)
        variables = [match[0] for match in matches]
        return variables

    def removeStrings(self):
        # Removes the strings in a single-line line. Multiline strings dealt with in other function
        if self.lineType == LineTypes.CONTINUES_MULTILINE_STRING:
            return ""
        strippedLine = LineHelpers.removeStrings(self.line)
        return self.removeMultilineString(strippedLine)

    def removeMultilineString(self, text=None):
        if text == None:
            text = self.line
        if self.lineType == LineTypes.STARTS_DOUBLE_MULTILINE_STRING:
            return self.removeMultilineHelper(text, start=True, token='"""')
        elif self.lineType == LineTypes.STARTS_SINGLE_MULTILINE_STRING:
            return self.removeMultilineHelper(text, start=True, token="'''")
        elif self.lineType == LineTypes.ENDS_DOUBLE_MULTILINE_STRING:
            return self.removeMultilineHelper(text, start=False, token='"""')
        elif self.lineType == LineTypes.ENDS_SINGLE_MULTILINE_STRING:
            return self.removeMultilineHelper(text, start=False, token="'''")
        else:
            return text

    def removeMultilineHelper(self, text, start=False, token='"""',):
        if start:
            commentStart = text.find(token)
            commentEnd = text[commentStart+1:].find(token)
            if commentEnd != -1:
                commentEnd += commentStart
                text = text[0:commentStart] + text[commentEnd+4:]
            else:
                text = text[0:commentStart]
        else:
            commentEnd = text.find(token)
            newLine = text[0:commentEnd+4]
        return text
