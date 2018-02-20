import re

class CodeLine:
    def __init__(self, line, lineNumber):
        self.line = line
        self.lineNumber = lineNumber

    def extractVariables(self):
        # A rudimentary method of parsing out variable names in this line. 
        # Relies on the variable being in the form: "variable = value"
        # This is not required in python but it's a decent way of getting
        # most of the variable names out of a line
        variables = re.findall(r"(([a-zA-Z_])\w*)([ \t])*=", self.line)
        variables = [match[0] for match in variables]
        return variables
