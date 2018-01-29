from CodeParser import CodeParser
from CodeFile import CodeFile
import os.path


parser = CodeParser()
codeFile = CodeFile()

parentDirectory = os.path.split(os.path.dirname(__file__))[0]
path = os.path.join(parentDirectory, '..', 'example.py')
codeFile.parseFile(path)


print("=== CLASSES:")
for i in codeFile.classes:
    print(i)

print("=== FUNCTIONS:")
for i in codeFile.functions:
    print(i)


