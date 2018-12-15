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
        self.assertEqual(len(function.variables), len(args))
        for i in range(len(args)):
            self.assertEqual(function.variables[i].name, args[i])
            self.assertEqual(function.variables[i].line_number, lineNumber)


if __name__ == '__main__':
    unittest.main()
