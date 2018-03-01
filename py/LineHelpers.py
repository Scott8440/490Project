import re

def stripLine(line):
    return removeStrings(removeComment(line))

def removeComment(line):
    noStrings = removeStrings(line)
    commentLocation = noStrings.find("#") 
    if commentLocation > -1:
        commentLocation += len(line) - len(noStrings)
        return line[0:commentLocation]
    return line

def removeStrings(line):
    # Removes the strings in a single-line line. Multiline strings dealt with in other function
    stringMatcher = r"('(?!'')(?!')(?<!'').*?(?<!\\)('|\\$))|(\"(?!\"\")(?!\")(?<!\"\").*?(?<!\\)(\"|\\$))"
    stringMatcher = re.compile(stringMatcher, re.MULTILINE)
    strippedLine = re.sub(stringMatcher, '', line)

    # removes a mulitiline string that's on a single line like this """ string """
    multiStringMatcher = r"('''.*?(?<!\\)(''|\\$))|(\"\"\".*?(\"\"\"|\\$))"
    mutliStringMatcher = re.compile(multiStringMatcher, re.MULTILINE)
    strippedLine = re.sub(multiStringMatcher, '', strippedLine)
    
    # stringMatcher = r"('(?!'')(?!')(?<!'').*?(?<!\\)'|\"(?!\"\")(?!\")(?<!\"\")(?!\").*?(?<!\\)\")"
    return strippedLine
    
def removeMultilineString(line):
    commentStart = None
    commentEnd = None
    quoteChar = None
    stringsLeft = True
    while stringsLeft:
        stringsLeft = False
        if ("'''" in line):
            commentStart = line.find("'''")
            quoteChar = "'''"
        elif ('"""' in line):
            commentStart = line.find('"""')
            quoteChar = '"""' 
        if commentStart is not None:
            stringsLeft = True
            commentEnd = line[commentStart+1:].find(quoteChar)
            if commentEnd > commentStart:
                commentEnd += commentStart
                line = line[0:commentStart] + line[commentEnd+4:]
            else:
                line = line[:commentStart]
    return line

def findRealCharacter(line, char):
    line = removeStrings(line)
    return line.find(char)

def countRealCharacter(line, char):
    line = removeStrings(line)
    return line.count(char)
