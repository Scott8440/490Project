import re

def removeStrings(line):
    # Removes the strings in a single-line line. Multiline strings dealt with in other function
    stringMatcher = r"('(?!'')(?!')(?<!'').*?(?<!\\)('|\\$))|(\"(?!\"\")(?!\")(?<!\"\").*?(?<!\\)(\"|\\$))/gm"
    stringMatcherMultiline = re.compile(stringMatcher, re.MULTILINE)
    # stringMatcher = r"('(?!'')(?!')(?<!'').*?(?<!\\)'|\"(?!\"\")(?!\")(?<!\"\")(?!\").*?(?<!\\)\")"
    strippedLine = re.sub(stringMatcherMultiline, '', line)
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
