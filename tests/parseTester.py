from py.CodeParser import CodeParser
import os.path


parentDirectory = os.path.split(os.path.dirname(__file__))[0]
# path = 'example.py'
path = os.path.join(parentDirectory, '..', 'py', 'CodeParser.py')

parser = CodeParser(path)

codeFile = parser.parseFile()

print("=== CLASSES:")
for i in codeFile.classes:
    i.printSelf()

print("=== FUNCTIONS:")
for i in codeFile.functions:
    i.printSelf(level=0)

print("=== BLOCKS:")
for i in codeFile.blocks:
    i.printSelf()
