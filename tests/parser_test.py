import unittest
import os.path
from py.CodeParser import CodeParser
from py.CodeClass import CodeClass
from py.CodeFunction import CodeFunction
from py.CodeBlock import CodeBlock
from py.CodeLine import CodeLine, LineTypes


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

    def testMultilineFile(self):
        path = 'multiline_test_file.py'
        parser = CodeParser(path)
#        codedLines = parser.parseMultilines(1, 1, LineTypes.STARTS_SBRACE_LINE)
#        self.assertEqual(codedLines[0].lineType, LineTypes.STARTS_SBRACE_LINE)
#        self.assertEqual(codedLines[1].lineType, LineTypes.ENDS_SBRACE_LINE)
        # for i in codedLines:
        #    print(i.printLine())

#        codedLines = parser.parseMultilines(5, 1, LineTypes.STARTS_CBRACE_LINE)
#        self.assertEqual(codedLines[0].lineType, LineTypes.STARTS_CBRACE_LINE)
#        self.assertEqual(codedLines[1].lineType, LineTypes.ENDS_CBRACE_LINE)
#
#        codedLines = parser.parseMultilines(9, 1, LineTypes.STARTS_PARENTHESES_LINE)
#        self.assertEqual(codedLines[0].lineType, LineTypes.STARTS_PARENTHESES_LINE)
#        self.assertEqual(codedLines[1].lineType, LineTypes.ENDS_PARENTHESES_LINE)
#
        #codedLines = parser.parseMultilines(13, 1, LineTypes.STARTS_SBRACE_LINE)
        #print(codedLines)
        #self.assertEqual(codedLines[0].lineType, LineTypes.STARTS_PARENTHESES_LINE)
        #self.assertEqual(codedLines[1].lineType, LineTypes.ENDS_SBRACE_LINE)

        print("Parsing last segment")
        codedLines = parser.parseMultilines(16, 1, LineTypes.STARTS_SBRACE_LINE)
        for i in codedLines:
            i.printLine()
        self.assertEqual(codedLines[0].lineType, LineTypes.STARTS_SBRACE_LINE)
        self.assertEqual(codedLines[1].lineType, LineTypes.STARTS_PARENTHESES_LINE)
        self.assertEqual(codedLines[2].lineType, LineTypes.ENDS_PARENTHESES_LINE)
        self.assertEqual(codedLines[3].lineType, LineTypes.ENDS_SBRACE_LINE)

    def testEscapeNewlineFile(self):
        path = 'escape_newline_test_file.py'
        parser = CodeParser(path)
        logicalLines = parser.removeEscapeNewlines()
        self.assertEqual(len(logicalLines), 5)
        self.assertEqual(logicalLines[0][1], 1)
        self.assertEqual(logicalLines[1][1], 2)
        self.assertEqual(logicalLines[2][1], 4)
        self.assertEqual(logicalLines[3][1], 5)
        self.assertEqual(logicalLines[4][1], 14)
        print(logicalLines)

if __name__ == '__main__':
    unittest.main()
