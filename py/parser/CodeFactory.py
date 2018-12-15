from py.parser.PythonParser import PythonParser
from py.parser.CodeParser import FileTypeError


class CodeFactory:

    def createParser(filename):
        filetype = filename[filename.rfind('.')+1:]

        if filetype == 'py':
            return PythonParser(filename)
        # NOTE: This is how the factory can be expanded once more language
        # parsers are implemented
        # elif filetypye == 'js':
        #     return JavascriptParser(filename)
        else:
            raise FileTypeError
