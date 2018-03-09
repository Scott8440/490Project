
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
        self.logicalLines = self.removeEscapeNewlines()
        self.codedLines = self.codifyLines()
        self.currentCodedLineIndex = 0
        self.filename = filename

    def parseFile(self):
        raise NotImplementedError

    def parseBlock(self):
        raise NotImplementedError
