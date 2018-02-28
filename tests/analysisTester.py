from py.CodeParser import CodeParser
from py.analyzer.FileAnalyzer import FileAnalyzer

path = 'example.py'

parser = CodeParser(path)
codeFile = parser.parseFile()

analyzer = FileAnalyzer(codeFile)

analyzer.analyzeFile()
analyzer.printAlerts()
