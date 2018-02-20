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


if __name__ == '__main__':
    unittest.main()
