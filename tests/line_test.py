import unittest
from py.CodeLine import CodeLine
from py.LineTypes import LineTypes


class TestLineMethods(unittest.TestCase):

    lineNumber = 7 # Dummy lineNumber
    indentation = 1 # Dummy indentation

    def testLineCreation(self):
        string = "this is a line"
        line = CodeLine(string, self.lineNumber, self.indentation)
        self.assertEqual(line.line, string)
        self.assertEqual(line.lineNumber, self.lineNumber)

    def testBasicVariableParsing(self):
        string = "var = 2"
        line = CodeLine(string, self.lineNumber, self.indentation)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], "var")

    def testComplicatedVariableParsing(self):
        string = "self.x = x"
        line = CodeLine(string, self.lineNumber, self.indentation)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], "self.x")

    def testNoParseVariableInStringType(self):
        string = "var = 2" # Assume this has been parsed as a part of a multiline string
        line = CodeLine(string, self.lineNumber, self.indentation, LineTypes.CONTINUES_MULTILINE_STRING)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 0)

    def testRemoveSimpleString(self):
        string = "var = 'this is a string'"
        line = CodeLine(string, self.lineNumber, self.indentation)
        strippedLine = line.removeStrings()
        correctStrip = "var = "
        self.assertEqual(strippedLine, correctStrip)

    def testRemoveStringWithNoString(self):
        string = "var = x"
        line = CodeLine(string, self.lineNumber, self.indentation)
        stripped = line.removeStrings()
        self.assertEqual(line.line, stripped)

    def testRemoveStringWithEscapeChar(self):
        txtFile = open('escapeCharacterLine.txt', 'r')
        string = txtFile.readline().rstrip()
        txtFile.close()

        line = CodeLine(string, self.lineNumber, self.indentation)
        stripped = line.removeStrings()
        correctStrip = "var = "
        self.assertEqual(stripped, correctStrip)

    def testRemoveMultipleStrings(self):
        string = 'var1 = "hello", var2 = "goodbye"'
        line = CodeLine(string, self.lineNumber, self.indentation)
        stripped = line.removeStrings()
        correctStrip = 'var1 = , var2 = '
        self.assertEqual(stripped, correctStrip)

    def testRemoveStringThatDoesntEnd(self):
        string = 'var1 = "hello\\\n'
        line = CodeLine(string, self.lineNumber, self.indentation)
        stripped = line.removeStrings()
        correctStrip = 'var1 = \n'
        self.assertEqual(stripped, correctStrip)

    def testGetsVariableInStringStartType(self):
        string = 'multiline = """ start of string'
        line = CodeLine(string, self.lineNumber, self.indentation, LineTypes.STARTS_DOUBLE_MULTILINE_STRING)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testIgnoresStringVariableInStringStartType(self):
        string = 'multiline = """ var = x'
        line = CodeLine(string, self.lineNumber, self.indentation, LineTypes.STARTS_DOUBLE_MULTILINE_STRING)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variables[0], 'multiline')

    def testHandlesCompleteMultilineOnOneLine(self):
        string = 'multiline = """ bad_var = x """, var = x'
        line = CodeLine(string, self.lineNumber, self.indentation)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 2)
        self.assertEqual(variables[0], 'multiline')
        self.assertEqual(variables[1], 'var')


if __name__ == '__main__':
    unittest.main()
