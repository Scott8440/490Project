def hello(name):
    print("Hello, {}".format(name))

class exClass(parentClass):
    
    staticVar1 = None
    staticVar2 = None
    staticVar3 = None

    def __init__(self):
        pass

    def doThing(self, foo):
        print(foo + "")

print('random script things')
# Comments in this block
x = 5
y = x * 2
print(y)
# more comments
if True:
    print("inside an if block")
    x = 2
    y = 3
    if False:
        print("if block inside an if block")

def longArgs(arg1, arg2, arg3, arg4):
    print("{}".format(arg1 + arg2 + arg3 + arg4))
    if arg1:
        print(arg2)
    else:
        print(arg3)

def twoLineArgs(arg1, arg2, arg3,
                arg4, arg5, arg6):
    print("{}".format(arg1 + arg2 + arg3 + arg4))

def threeLineArgs(arg1, arg2,
                  arg3, arg4,
                  arg5, arg6):
    print("{} {}".format(arg1 + arg2, arg3 + arg4))
