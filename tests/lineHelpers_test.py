import unittest
import py.code_rep.LineHelpers as LineHelpers


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
        self.assertEqual(newLine, '')

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

    def testRemoveComment(self):
        line1 = "this line has no comment"
        newLine = LineHelpers.removeComment(line1)
        self.assertEqual(newLine, line1)

        line2 = "this line has a # comment"
        newLine = LineHelpers.removeComment(line2)
        correctLine = "this line has a "
        self.assertEqual(newLine, correctLine)

        line3 = "this line has a 'string' and # comment"
        newLine = LineHelpers.removeComment(line3)
        correctLine = "this line has a 'string' and "
        self.assertEqual(newLine, correctLine)

        line4 = "this line has a 'string with a # character'"
        newLine = LineHelpers.removeComment(line4)
        self.assertEqual(newLine, line4)

        line5 = "this line has a 'string # char' and # comment"
        newLine = LineHelpers.removeComment(line5)
        correctLine = "this line has a 'string # char' and "
        self.assertEqual(newLine, correctLine)

        line6 = "# only a comment"
        newLine = LineHelpers.removeComment(line6)
        correctLine = ""
        self.assertEqual(newLine, correctLine)


if __name__ == '__main__':
    unittest.main()
