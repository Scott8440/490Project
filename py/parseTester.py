from CodeParser import CodeParser
import os.path


parentDirectory = os.path.split(os.path.dirname(__file__))[0]
path = os.path.join(parentDirectory, '..', 'example2.py')
path = 'CodeParser.py'

parser = CodeParser(path)

codeFile = parser.parseFile()

print("=== CLASSES:")
for i in codeFile.classes:
    print(i)
    for j in i.lines:
        print("  {}".format(j.rstrip()))
    for j in i.memberFunctions:
        j.printSelf(level=2)

print("=== FUNCTIONS:")
for i in codeFile.functions:
    i.printSelf(level=0)

print("=== BLOCKS:")
for i in codeFile.blocks:
    i.printSelf()
