import py.code_rep.LineHelpers as LineHelpers
import re


def extractMagicNumbers(text):
    strippedText = LineHelpers.stripLine(text)
    # REGEX matches all numbers not following an equals sign or within a word
    
    #numberList = re.findall(r"(?<!=)(?<!= )((?<!\w)[-+]?\d*\.?\d+(?!\w))", strippedText)
    numberList = []
    intList = re.findall(r"(?<!=)(?<!= )(?<!\w)[-+]\d+", strippedText)
    floatList = re.findall(r"(?<!=)(?<!= )(?<!\w)[-+]\d+\.\d+(?!\w)", strippedText)
    for i in intList:
        numberList.append(int(i))
    for i in floatList:
        numberList.append(float(i))
    return numberList

