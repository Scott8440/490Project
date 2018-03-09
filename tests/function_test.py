import unittest
from py.code_rep.CodeFunction import CodeFunction

class TestFunctionMethods(unittest.TestCase):

    def testFunctionCreation(self):
        name = 'testFunction'
        args = ['arg1', 'arg2', 'arg3']
        lineNumber = 10
        function = CodeFunction(name, args, lineNumber)
        self.assertEqual(function.name, name)
        self.assertEqual(function.arguments, args)
        self.assertEqual(function.lineNumber, lineNumber)
        argsWithLineNumbers = {'arg1': 10, 'arg2': 10, 'arg3': 10}
        self.assertEqual(function.variables, argsWithLineNumbers)

if __name__ == '__main__':
    unittest.main()
