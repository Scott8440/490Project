from py.CodeLine import LineTypes

def removeStrings(line):
    # Removes the strings in a single-line line. Multiline strings dealt with in other function
    stringStart = None
    stringChar = None
    stringsLeft = True
    newLine = line
    lineLength = len(newLine)
    while stringsLeft:
        i = 0
        stringsLeft = False
        while i < lineLength:
            char = newLine[i]
            if char == '"' or char == "'":
                # Skips this if it is actually a multiline signifier
                if newLine[i:i+3] == char*3:
                    i += 3    
                else:
                    stringChar = char
                    stringStart = i 
                    stringsLeft = True
                    break
            i += 1
        if stringStart is not None:
            index = i+1
            stringEnd = stringStart
            while index < lineLength and newLine[index] != stringChar:
                char = newLine[index]
                if char == "\\":
                    index += 1
                index += 1
            stringEnd = index
            newLine = newLine[:stringStart] + newLine[stringEnd+1:]
    return removeMultilineString(newLine)

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
    line = removeString(line)
    return line.find(char)

def determineLineType(line, prevLineType):
    newType = None
    if (prevLineType == LineTypes.STARTS_PARENTHESES_LINE or 
        prevLineType == LineTypes.CONTINUES_PARENTHESES_LINE):
        # Look for ending )
        if findRealCharacter(line, ')') > -1:
            newType = LineTypes.ENDS_PARENTHESES_LINE
        newType = LineTypes.CONTINUES_PARENTHESES_LINE

    elif (prevLineType == LineTypes.STARTS_CBRACE_LINE or
          prevLineType == LineTypes.CONTINUES_CBRACE_LINE):
        # look for ending ]
        if findRealCharacter(line, ']') > -1:
            newType = LineTypes.ENDS_SBRACE_LINE
        newType = LineTypes.CONTINUES_SBRACE_LINE

    elif (prevLineType == LineTypes.STARTS_SBRACE_LINE or
          prevLineType == LineTypes.CONTINUES_SBRACE_LINE):
        # look for ending }
        if findRealCharacter(line, '}') > -1:
            newType = LineTypes.ENDS_SBRACE_LINE
        newType = LineTypes.CONTINUES_SBRACE_LINE

    #TODO: Add other multiline type
    elif (prevLineType == LineTypes.STARTS_MULTILINE_STRING or
          prevLineType == LineTypes.CONTINUES_MULTILINE_STRING):
        # look for eding """
        if findRealCharacter(line, '"""') > -1:
            newType = LineTypes.ENDS_SBRACE_LINE
        newType = LineTypes.CONTINUES_SBRACE_LINE
    
    elif (prevLineType == LineTypes.STARTS_SINGLE_QUOTE_STRING or
          prevLineType == LineTypes.CONTINUES_SINGLE_QUOTE_STRING):
        # look for ending '
        if findRealCharacter(line, '\'') > -1:
            newType = LineTypes.ENDS_SBRACE_LINE
        newType = LineTypes.CONTINUES_SBRACE_LINE

    elif (prevLineType == LineTypes.STARTS_DOUBLE_QUOTE_STRING or
          prevLineType == LineTypes.CONTINUES_DOUBLE_QUOTE_STRING):
        # look for ending "
        if findRealCharacter(line, '"') > -1:
            newType = LineTypes.ENDS_SBRACE_LINE
        newType = LineTypes.CONTINUES_SBRACE_LINE

    else:
        # determine type regularly
        pass
    pass
    x = ( " a
            )b)
            "
        )
