from py.parser.PythonParser import PythonParser
from py.analyzer.FileAnalyzer import FileAnalyzer
from py.analyzer.AnalysisParameters import AnalysisParameters
from py.parser.CodeParser import FileTypeError
from py.parser.CodeFactory import CodeFactory
import os
import glob
import sys
import argparse


def getDirectories(baseDir):
    dirs = []
    for name in os.listdir(baseDir):
        if os.path.isdir(os.path.join(baseDir, name)):
            dirs.append(os.path.join(baseDir, name))
    return dirs

def getFiles(baseDir):
    files = []
    for name in os.listdir(baseDir):
        if os.path.isfile(os.path.join(baseDir, name)):
            files.append(os.path.join(baseDir, name))
    return files

def analyzeDirectory(path, recursive=False, parameters=None):
    pythonFiles = os.path.join(path, "*")
    fileList = getFiles(path)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    for i in fileList:
        rel_path = i
        filePath = os.path.join(script_dir, rel_path)
        analyzeFile(filePath, parameters=parameters)
    if recursive:
        directories = getDirectories(path)
        for i in directories:
            analyzeDirectory(i, recursive=recursive, parameters=parameters)

def analyzeFile(path, parameters=None):
    parser = CodeFactory()
    try:
        parser = CodeFactory.createParser(path)
    except FileTypeError:
        return
    codeFile = parser.parseFile()
    analyzer = FileAnalyzer(codeFile, parameters=parameters)
    analyzer.analyzeFile()
    analyzer.printAlerts()
    
def makePath(fileName):
    current_dir = os.getcwd()
    return(os.path.join(current_dir, fileName))

def isValidFilename(filename):
    return len(filename) <= 3 and filename[-3:] != ".py"

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--params", help='location of the parameter specification file. Default parameters will be used if this option is not set.')
    parser.add_argument("-r", '--recursive', action='store_true', help='if set, each directory listed will be recursively traversed and all files will be analyzed.')
    parser.add_argument("files", nargs="+", help="one or more files/directories to be analyzed.")
    return parser.parse_args()

def execute():
    args = parseArguments()
    parameters = AnalysisParameters()
    if args.params:
        parameters.constructFromFile(args.params)
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    for filename in args.files:
        if os.path.isdir(os.path.join(script_dir, filename)):
            analyzeDirectory(os.path.join(script_dir, filename), recursive=args.recursive, parameters=parameters)
        else:
            path = makePath(filename)
            analyzeFile(path, parameters=parameters)


if __name__ == '__main__':
    execute()
