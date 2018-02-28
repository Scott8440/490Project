from py.analyzer.CodeAnalyzer import CodeAnalyzer


class ClassAnalyzer(CodeAnalyzer):

    def __init__(self, codeClass, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.codeClass = codeClass

    def analyzeClass(self):
        pass
