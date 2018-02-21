import unittest
import os.path
from py.CodeParser import CodeParser
from py.CodeClass import CodeClass
from py.CodeFunction import CodeFunction
from py.CodeBlock import CodeBlock
from py.CodeLine import CodeLine, LineTypes


class TestParser(unittest.TestCase):

    def testExampleFile(self):
        parentDirectory = os.path.split(os.path.dirname(__file__))[0]
        path = os.path.join(parentDirectory, '..', 'example.py')
        parser = CodeParser(path)
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
        self.assertEqual(len(codeFile.blocks), 5)
if __name__ == '__main__':
    unittest.main()
