if (True and False or True
    and False):
    print("if statement")
    x = 2
    if (False or True or False
        or False or False):
        print("if inside an if")
        y = 2

def func2(arg1):
    return True

def endOfBlock(self, indentation, beginningIndentation, minDifference, line):
    return not(self.notEndOfFile() and indentation >= beginningIndentation + minDifference)

def func(arg1):
    x = 1
    if (x == 1):
        print(x+1)
        print(x)
    else:
        print(y)

def multilineString():
    w = """ hello this is a multiline
        string which has
        3 lines """

    x = """ tricky string """

    y = """
        starting a block inside string:
        def funcTricky():
            string
        """
    z = '''
        string type 2
        '''
    print(x)

def functionWithMixedTabsAndSpaces():
    thisLineHasOneTab = None
    thisLineHas4Spaces = None
    if(thisLineHas4Spaces): # this line has 4 spaces
        thisLineHasTwoTabs = None

def functionSplitWithComment():
    x = 2
# weirdly placed comment
    y = 3



