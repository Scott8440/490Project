from py.CodeParser import CodeParser
from py.analyzer.FileAnalyzer import FileAnalyzer
import os
import glob
import sys


def analyzeDirectory():
    fileList = glob.glob("*.py")
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    for i in fileList:
        rel_path = i
        path = os.path.join(script_dir, rel_path)
        analyzeFile(path)


def analyzeFile(path):
    parser = CodeParser(path)
    codeFile = parser.parseFile()
    analyzer = FileAnalyzer(codeFile)
    analyzer.analyzeFile()
    analyzer.printAlerts()

def makePath(fileName):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    return(os.path.join(script_dir, fileName))


if sys.argv[1]:
    fileName = sys.argv[1]
    path = makePath(fileName) 
    analyzeFile(path)
else:
    analyzeDirectory()




