from py.parser.CodeParser import CodeParser
from py.analyzer.FileAnalyzer import FileAnalyzer
from py.analyzer.AnalysisParameters import AnalysisParameters
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
    #script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    current_dir = os.getcwd()
    return(os.path.join(current_dir, fileName))


print(sys.argv)
if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        if len(filename) <= 3 or filename[-3:] != ".py":
            continue
        path = makePath(filename) 
        analyzeFile(path)
else:
    analyzeDirectory()

