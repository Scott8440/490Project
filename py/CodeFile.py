from CodeParser import CodeParser

class CodeFile:

    def __init__(self):
        self.filename = ''
        self.functions = []
        self.classes = []
        self.blocks = []

    def parseFile(self, filename):
       codeParser = CodeParser()
       with open(filename) as f:
            lines = f.readlines()
            lineNum = 0
            while lineNum < len(lines):
                line = lines[lineNum]
                if 'class' in line.split(' '):
                    print("****Parsing CodeClass: {}".format(line.rstrip()))
                    classLines, lineNum = codeParser.packageBlock(lines, lineNum)
                    self.classes.append(codeParser.parseClass(classLines))
                elif 'def' in line.split(' '):
                    print("****Parsing CodeFunction: {}".format(line.rstrip()))
                    functionLines, lineNum = codeParser.packageBlock(lines, lineNum)
                    self.functions.append(codeParser.parseFunction(functionLines))
                else:
                    print("Random Line: '{}'".format(line.rstrip()))
                    lineNum += 1
                line = f.readline()
