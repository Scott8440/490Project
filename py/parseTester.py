from CodeParser import CodeParser
import os.path


parentDirectory = os.path.split(os.path.dirname(__file__))[0]
#path = os.path.join(parentDirectory, '..', 'example.py')
path = 'CodeParser.py'

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
        for k in j.blocks:
            print("    {}".format(k))

print("=== FUNCTIONS:")
for i in codeFile.functions:
    print(i)
    print("  Name: '{}'".format(i.name))
    print("  Args: {}".format(i.arguments))
    for j in i.lines:
        print("  {}".format(j.rstrip()))
    for j in i.blocks:
        print("  {}".format(j))

print("=== BLOCKS:")
for i in codeFile.blocks:
    #print("{}: {}".format(i, i.getLength()))
    #print(i.blockType)
    #print("LINES:")
    #for j in i.lines:
    #    print(j.strip())
    #print("BLOCKS:")
    #for j in i.childrenBlocks:
    #    print("  {}".format(j))
    #print("====")
    i.printSelf()
