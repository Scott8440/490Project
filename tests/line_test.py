import unittest
from py.CodeLine import CodeLine, LineTypes


class TestLineMethods(unittest.TestCase):

    lineNumber = 7 #Dummy lineNumber
    def testLineCreation(self):
        string = "this is a line"
        line = CodeLine(string, self.lineNumber)
        self.assertEqual(line.line, string)
        self.assertEqual(line.lineNumber, self.lineNumber)

    def testBasicVariableParsing(self):
        string = "var = 2"
        line = CodeLine(string, self.lineNumber)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], "var")

    def testNoParseVariableInStringType(self):
        string = "var = 2" # Assume this has been parsed as a part of a multiline string
        line = CodeLine(string, self.lineNumber, LineTypes.STRING)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 0)

    def testRemoveSimpleString(self):
        string = "var = 'this is a string'"
        line = CodeLine(string, self.lineNumber)
        strippedLine = line.removeString()
        correctStrip = "var = "
        self.assertEqual(strippedLine, correctStrip)

    def testRemoveStringWithNoString(self):
        string = "var = x"
        line = CodeLine(string, self.lineNumber)
        stripped = line.removeString()
        self.assertEqual(line.line, stripped)

    def testRemoveStringWithEscapeChar(self):
        txtFile = open('escapeCharacterLine.txt', 'r')
        string = txtFile.readline().rstrip()
        txtFile.close()

        line = CodeLine(string, self.lineNumber)
        stripped = line.removeString()
        correctStrip = "var = "
        self.assertEqual(stripped, correctStrip)

    def testRemoveMultipleStrings(self):
        string = 'var1 = "hello", var2 = "goodbye"'
        line = CodeLine(string, self.lineNumber)
        stripped = line.removeString()
        correctStrip = 'var1 = , var2 = '
        self.assertEqual(stripped, correctStrip)

    def testRemoveStringThatDoesntEnd(self):
        string = 'var1 = "hello'
        line = CodeLine(string, self.lineNumber)
        stripped = line.removeString()
        correctStrip = 'var1 = '
        self.assertEqual(stripped, correctStrip)

    def testGetsVariableInStringStartType(self):
        string = 'multiline = """ start of string'
        line = CodeLine(string, self.lineNumber, LineTypes.MULTILINE_STRING_START)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testIgnoresStringVariableInStringStartType(self):
        string = 'multiline = """ var = x'
        line = CodeLine(string, self.lineNumber, LineTypes.MULTILINE_STRING_START)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testHandlesCompleteMultilineOnOneLine(self):
        string = 'multiline = """ bad_var = x """, var = x'
        line = CodeLine(string, self.lineNumber)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0], 'multiline')
        self.assertEqual(variables[1], 'var')

if __name__ == '__main__':
    unittest.main()
