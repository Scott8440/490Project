import unittest
from py.CodeLine import CodeLine, LineTypes


class TestLineMethods(unittest.TestCase):

    def testLineCreation(self):
        string = "this is a line"
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        self.assertEqual(line.line, string)
        self.assertEqual(line.lineNumber, lineNumber)

    def testBasicVariableParsing(self):
        string = "var = 2"
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], "var")

    def testNoParseVariableInStringType(self):
        string = "var = 2" # Assume this has been parsed as a part of a multiline string
        lineNumber = 7
        line = CodeLine(string, lineNumber, LineTypes.STRING)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 0)

    def testRemoveSimpleString(self):
        string = "var = 'this is a string'"
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        strippedLine = line.removeString()
        correctStrip = "var = "
        self.assertEqual(strippedLine, correctStrip)

    def testRemoveStringWithNoString(self):
        string = "var = x"
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        stripped = line.removeString()
        self.assertEqual(line.line, stripped)

    def testRemoveStringWithEscapeChar(self):
        txtFile = open('escapeCharacterLine.txt', 'r')
        string = txtFile.readline().rstrip()
        txtFile.close()

        lineNumber = 7
        line = CodeLine(string, lineNumber)
        stripped = line.removeString()
        correctStrip = "var = "
        self.assertEqual(stripped, correctStrip)

    def testGetsVariableInStringStartType(self):
        string = 'multiline = """ start of string'
        lineNumber = 7
        line = CodeLine(string, lineNumber, LineTypes.STRING_START)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testIgnoresStringVariableInStringStartType(self):
        string = 'multiline = """ var = x'
        lineNumber = 7
        line = CodeLine(string, lineNumber, LineTypes.STRING_START)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testHandlesCompleteMultilineOnOneLine(self):
        string = 'multiline = """ bad_var = x """, var = x'
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0], 'multiline')
        self.assertEqual(variables[1], 'var')


if __name__ == '__main__':
    unittest.main()
