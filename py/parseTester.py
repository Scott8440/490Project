from CodeParser import CodeParser
import os.path


parentDirectory = os.path.split(os.path.dirname(__file__))[0]
path = os.path.join(parentDirectory, '..', 'example.py')

parser = CodeParser(path)

codeFile = parser.parseFile()

print("=== CLASSES:")
for i in codeFile.classes:
    print(i)
    for j in i.lines:
        print("  {}".format(j.rstrip()))
    for j in i.memberFunctions:
        print("  {}".format(j))
        for k in j.lines:
            print("    {}".format(k.rstrip()))

print("=== FUNCTIONS:")
for i in codeFile.functions:
    print(i)
    print("  Name: '{}'".format(i.name))
    print("  Args: {}".format(i.arguments))
    for j in i.lines:
        print("  {}".format(j.rstrip()))

print("=== BLOCKS:")
for i in codeFile.blocks:
    print(i)
    print("====")
