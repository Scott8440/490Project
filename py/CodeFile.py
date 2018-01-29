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
            line = f.readline()
            while line:
                if 'class' in line.split(' '):
                    print("****Parsing CodeClass: {}".format(line))
                    classLines = codeParser.packageBlock(f, line)
                    self.classes.append(codeParser.parseClass(classLines))
                elif 'def' in line.split(' '):
                    print("****Parsing CodeFunction: {}".format(line))
                    functionLines = codeParser.packageBlock(f, line)
                    self.functions.append(codeParser.parseFunction(functionLines))
                else:
                    print(line, end='')
                line = f.readline()
