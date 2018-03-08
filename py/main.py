from py.parser.CodeParser import CodeParser
from py.analyzer.FileAnalyzer import FileAnalyzer
from py.analyzer.AnalysisParameters import AnalysisParameters
import os
import glob
import sys


def getDirectories(baseDir):
    dirs = []
    for name in os.listdir(baseDir):
        if os.path.isdir(os.path.join(baseDir, name)):
            dirs.append(name)
    return dirs

def analyzeDirectory(path, recursive=False):
    pythonFiles = os.path.join(path, "*.py")
    fileList = glob.glob(pythonFiles)
    for i in fileList:
        rel_path = i
        filePath = os.path.join(script_dir, rel_path)
        analyzeFile(filePath)
    directories = getDirectories(path)
    for i in directories:
        analyzeDirectory(i, recursive=True)

def analyzeFile(path):
    parser = CodeParser(path)
    codeFile = parser.parseFile()
    analyzer = FileAnalyzer(codeFile)
    analyzer.analyzeFile()
    analyzer.printAlerts()

def makePath(fileName):
    current_dir = os.getcwd()
    return(os.path.join(current_dir, fileName))

def isValidFilename(filename):
    return len(filename) <= 3 and filename[-3:] != ".py"

if len(sys.argv) > 1:
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    for name in sys.argv[1:]:
        if os.path.isdir(os.path.join(script_dir, name)):
            analyzeDirectory(os.path.join(script_dir, name), recursive=True)
        else:
            path = makePath(name)
            analyzeFile(path)
else:
    analyzeDirectory('parser')

