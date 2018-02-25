import unittest
import os.path
from py.CodeLine import CodeLine, LineTypes
import py.LineHelpers as LineHelpers


class TestLineHelpers(unittest.TestCase):

    def testRemoveStrings(self):

        line1 = "this has no string"
        newLine = LineHelpers.removeStrings(line1)
        self.assertEqual(line1, newLine)

        line2 = "this has a 'string'"
        newLine = LineHelpers.removeStrings(line2)
        correctLine = "this has a "
        self.assertEqual(correctLine, newLine)

        line3 = "this 'string' has 'multiple' strings"
        newLine = LineHelpers.removeStrings(line3)
        correctLine = "this  has  strings"
        self.assertEqual(correctLine, newLine)

        line4 = r"this 'string\' is escaped"
        newLine = LineHelpers.removeStrings(line4)
        self.assertEqual(newLine, line4) 

        line5 = r'this "string\" is escaped'
        newLine = LineHelpers.removeStrings(line5)
        self.assertEqual(newLine, line5)

        line6 = r'""" multiline string """'
        newLine = LineHelpers.removeStrings(line6)
        self.assertEqual(newLine, line6)

        line7 = r'""" multiline start'
        newLine = LineHelpers.removeStrings(line7)
        self.assertEqual(newLine, line7)

        line8 = r'multiline end """'
        newLine = LineHelpers.removeStrings(line8)
        self.assertEqual(newLine, line8)

        line9 = "this 'string does not end \\"
        newLine = LineHelpers.removeStrings(line9)
        correctLine = "this "
        self.assertEqual(newLine, correctLine)

        line10 = "this 'string does not end \\\nnext line"
        newLine = LineHelpers.removeStrings(line10)
        correctLine = "this \nnext line"
        self.assertEqual(newLine, correctLine)

if __name__ == '__main__':
    unittest.main()
