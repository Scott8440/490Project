import unittest
from py.parser.CodeFactory import CodeFactory
from py.code_rep.CodeClass import CodeClass
from py.code_rep.CodeFunction import CodeFunction
from py.code_rep.CodeBlock import CodeBlock
from py.code_rep.CodeLine import CodeLine
from py.code_rep.LineTypes import LineTypes
import py.code_rep.LineHelpers as LineHelpers


class TestParser(unittest.TestCase):


    def testExampleFile(self):
        path = 'example.py'
        parser = CodeFactory.createParser(path)
        codeFile = parser.parseFile()

        # Check Functions
        functions = codeFile.functions
        self.assertEqual(len(functions), 5)
        func1Name = 'hello'
        func1Args = ['name']
        self.assertEqual(functions[0].name, func1Name)
        self.assertEqual(functions[0].arguments, func1Args)

        # Check Classes
        self.assertEqual(len(codeFile.classes), 1)

        # Check Blocks
        self.assertEqual(len(codeFile.blocks), 1)

        # Check Lines
        self.assertEqual(len(codeFile.lines), 6)

    def testMultilineFile(self):
        path = 'multiline_test_file.py'
        parser = CodeFactory.createParser(path)
        segmentLength = parser.parseMultilines(1, 1)
        self.assertEqual(segmentLength, 2)

        segmentLength = parser.parseMultilines(4, 1)
        self.assertEqual(segmentLength, 2)

        segmentLength = parser.parseMultilines(7, 1)
        self.assertEqual(segmentLength, 2)

        segmentLength = parser.parseMultilines(10, 1)
        self.assertEqual(segmentLength, 2)

        segmentLength = parser.parseMultilines(12, 1)
        self.assertEqual(segmentLength, 4)

    def testEscapeNewlineFile(self):
        path = 'escape_newline_test_file.py'
        parser = CodeFactory.createParser(path)
        logicalLines = parser.removeEscapeNewlines()
        self.assertEqual(len(logicalLines), 5)
        self.assertEqual(logicalLines[0][1], 1)
        self.assertEqual(logicalLines[1][1], 2)
        self.assertEqual(logicalLines[2][1], 4)
        self.assertEqual(logicalLines[3][1], 5)
        self.assertEqual(logicalLines[4][1], 14)

    def testCodifyLines(self):
        path = 'multiline_test_file.py'
        parser = CodeFactory.createParser(path)
        parser.logicalLines = parser.removeEscapeNewlines()
        codedLines = parser.codifyLines()
        self.assertEqual(codedLines[0].lineNumber,1) # check that line numbers are not 0-indexed
        self.assertEqual(codedLines[0].indentation, 0)
        self.assertEqual(codedLines[1].indentation, 4)
        self.assertEqual(codedLines[2].indentation, 4) # indentation remains same throughout multiline segment
        self.assertEqual(codedLines[3].indentation, 0)
        self.assertEqual(codedLines[4].indentation, 4)
        self.assertEqual(codedLines[5].indentation, 4)


        self.assertEqual(codedLines[6].indentation, 0)
        self.assertEqual(codedLines[7].indentation, 4)
        self.assertEqual(codedLines[8].indentation, 4)
        self.assertEqual(codedLines[17].indentation, 4)
        self.assertEqual(codedLines[18].indentation, 4)

        self.assertEqual(codedLines[18].indentation, 4)
        self.assertEqual(codedLines[18].lineType, LineTypes.STARTS_DOUBLE_MULTILINE_STRING)
        self.assertEqual(codedLines[19].indentation, 4)
        self.assertEqual(codedLines[20].indentation, 4)
        self.assertEqual(codedLines[19].lineType, LineTypes.CONTINUES_MULTILINE_STRING)

        self.assertEqual(codedLines[20].lineType, LineTypes.ENDS_DOUBLE_MULTILINE_STRING)

if __name__ == '__main__':
    unittest.main()
