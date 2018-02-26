import unittest
import os.path
from py.CodeParser import CodeParser
from py.CodeClass import CodeClass
from py.CodeFunction import CodeFunction
from py.CodeBlock import CodeBlock
from py.CodeLine import CodeLine
from py.LineTypes import LineTypes
import py.LineHelpers as LineHelpers


class TestParser(unittest.TestCase):


    # def testExampleFile(self):
    #    parentDirectory = os.path.split(os.path.dirname(__file__))[0]
    #    path = os.path.join(parentDirectory, '..', 'example.py')
    #    parser = CodeParser(path)
    #    codeFile = parser.parseFile()
#
#        # Check Functions
#        functions = codeFile.functions
#        self.assertEqual(len(functions), 5)
#        func1Name = 'hello'
#        func1Args = ['name']
#        self.assertEqual(functions[0].name, func1Name)
#        self.assertEqual(functions[0].arguments, func1Args) 
#
#        # Check Classes
#        self.assertEqual(len(codeFile.classes), 1)
#
#        # Check Blocks
#        self.assertEqual(len(codeFile.blocks), 5)

    # def testMultilineFile(self):
    #     print("test multilineFile")
    #     path = 'multiline_test_file.py'
    #     parser = CodeParser(path)
    #     segmentLength = parser.parseMultilines(1, 1)
    #     self.assertEqual(segmentLength, 2)

    #     segmentLength = parser.parseMultilines(5, 1)
    #     self.assertEqual(segmentLength, 2)

    #     segmentLength = parser.parseMultilines(9, 1)
    #     self.assertEqual(segmentLength, 2)

    #     segmentLength = parser.parseMultilines(13, 1)
    #     self.assertEqual(segmentLength, 2)

    #     segmentLength = parser.parseMultilines(16, 1)
    #     self.assertEqual(segmentLength, 4)

    # def testEscapeNewlineFile(self):
    #     print("test escapeNewlineFile")
    #     path = 'escape_newline_test_file.py'
    #     parser = CodeParser(path)
    #     logicalLines = parser.removeEscapeNewlines()
    #     self.assertEqual(len(logicalLines), 5)
    #     self.assertEqual(logicalLines[0][1], 1)
    #     self.assertEqual(logicalLines[1][1], 2)
    #     self.assertEqual(logicalLines[2][1], 4)
    #     self.assertEqual(logicalLines[3][1], 5)
    #     self.assertEqual(logicalLines[4][1], 14)


    def testCodifyLines(self):
        print("testCodifyLines")
        path = 'multiline_test_file.py'
        parser = CodeParser(path)
        parser.logicalLines = parser.removeEscapeNewlines()
        codedLines = parser.codifyLines()
        for i in range(len(codedLines)):
            print("{}".format(i))
            codedLines[i].printLine()
        self.assertEqual(codedLines[0].lineNumber,1) # check that line numbers are not 0-indexed
        self.assertEqual(codedLines[0].indentation, 0)
        self.assertEqual(codedLines[1].indentation, 4)
        self.assertEqual(codedLines[2].indentation, 4) # indentation remains same throughout multiline segment
        self.assertEqual(codedLines[16].indentation, 4)
        self.assertEqual(codedLines[17].indentation, 4)
        self.assertEqual(codedLines[18].indentation, 4)
        self.assertEqual(codedLines[19].indentation, 4)

        self.assertEqual(codedLines[25].lineType, LineTypes.STARTS_DOUBLE_MULTILINE_STRING)
        self.assertEqual(codedLines[25].indentation, 4) 
        self.assertEqual(codedLines[26].indentation, 4) 
        self.assertEqual(codedLines[27].indentation, 4) 
        self.assertEqual(codedLines[26].lineType, LineTypes.CONTINUES_MULTILINE_STRING)
        
        self.assertEqual(codedLines[27].lineType, LineTypes.ENDS_DOUBLE_MULTILINE_STRING)

if __name__ == '__main__':
    unittest.main()
