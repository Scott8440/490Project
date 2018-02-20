import unittest
from py.CodeLine import CodeLine


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

    def testNoParseVariableInString(self):
        string = "string = 'var = 2'"
        lineNumber = 7
        line = CodeLine(string, lineNumber)
        variables = line.extractVariables()
        self.assertEqual(len(variables), 1)
        self.assertEqual(variable[0], 'string')


if __name__ == '__main__':
    unittest.main()
