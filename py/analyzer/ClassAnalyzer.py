from py.analyzer.CodeAnalyzer import CodeAnalyzer
from py.analyzer.FunctionAnalyzer import FunctionAnalyzer
from py.analyzer.BlockAnalyzer import BlockAnalyzer
from py.analyzer.LineAnalyzer import LineAnalyzer
from py.analyzer.ClassCohesionAlert import ClassCohesionAlert


class ClassAnalyzer(CodeAnalyzer):

    def __init__(self, codeClass, parameters=None):
        CodeAnalyzer.__init__(self, parameters=parameters)
        self.codeClass = codeClass

    def analyzeClass(self):
        for codeFunction in self.codeClass.functions:
            functionAnalyzer = FunctionAnalyzer(codeFunction, parameters=self.params)
            functionAnalyzer.analyzeFunction()
            self.gatherAlerts(functionAnalyzer)

        for codeBlock in self.codeClass.childrenBlocks:
            blockAnalyzer = BlockAnalyzer(codeBlock, parameters=self.params)
            blockAnalyzer.analyzeBlock()
            self.gatherAlerts(blockAnalyzer)

        for codeLine in self.codeClass.lines:
            lineAnalyzer = LineAnalyzer(codeLine, parameters=self.params)
            lineAnalyzer.analyzeLine()
            self.gatherAlerts(lineAnalyzer)

        self.analyzeClassCohesion()

    def analyzeClassCohesion(self):
        if len(self.codeClass.functions) < self.params.minNumberClassFunctionsForCohesionAnalysis:
            return
        self.calculateClassCohesion()

    def calculateClassCohesion(self):
        functionAccessRatios = self.getFunctionAccessRatios()
        noAccessFunctions = []
        for function in functionAccessRatios:
            if function[1] == 0:
                noAccessFunctions.append(function[0])
        if len(noAccessFunctions)/len(self.codeClass.functions) > self.params.classCohesionLimit:
            self.addAlert(ClassCohesionAlert(self.codeClass.name, noAccessFunctions, self.codeClass.lineNumber))
       
    def getFunctionAccessRatios(self):
        if len(self.codeClass.memberVariables) == 0:
            return []
        functionAccessRatios = []
        for function in self.codeClass.functions:
            accessedMemberVars = function.getAccessedAttributes(self.codeClass.memberVariables)
            accessedFunctions = function.getAccessedAttributes(self.codeClass.getFunctionNames())
            for subFunctionName in accessedFunctions:
                if subFunctionName != function.name:
                    subFunction = self.codeClass.getFunction(subFunctionName)
                    subAccessedVars = subFunction.getAccessedAttributes(self.codeClass.memberVariables)
                    accessedMemberVars.update(subAccessedVars)
            ratio = len(accessedMemberVars)/len(self.codeClass.memberVariables)
            functionAccessRatios.append((function.name,ratio))
        return functionAccessRatios




