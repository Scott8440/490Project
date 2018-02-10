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
