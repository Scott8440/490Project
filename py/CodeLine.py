import re
from enum import Enum

class LineTypes(Enum):
    REGULAR, COMMENT, STRING, = range(1,4)

class CodeLine:

    lineTypes = Enum('lineTypes', 'REGULAR, COMMENT, STRING')
    #class lineTypes(Enum):
    #    REGULAR, COMMENT, STRING = range(1,4)

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
            variables = re.findall(r"(([a-zA-Z_])\w*)([ \t])*=", self.line)
            variables = [match[0] for match in variables]
        return variables
