from py.CodeParser import CodeParser
from py.analyzer.FileAnalyzer import FileAnalyzer
import os

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "../py/CodeParser.py"
path = os.path.join(script_dir, rel_path)


parser = CodeParser(path)
codeFile = parser.parseFile()

analyzer = FileAnalyzer(codeFile)

analyzer.analyzeFile()
analyzer.printAlerts()
