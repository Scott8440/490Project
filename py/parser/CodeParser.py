
class Error(Exception):
    pass

class FileTypeError(Error):
    def __init__(self):
       self.message = "Trying to parse a file of the wrong type" 

class CodeParser:

    def __init__(self, filename):
        with open(filename, 'r') as f:
            self.lines = f.readlines()
            self.numLines = len(self.lines)
        self.filename = filename

    def parseFile(self):
        raise NotImplementedError
