import py.code_rep.LineHelpers as LineHelpers
import re


def extractMagicNumbers(text):
    strippedText = LineHelpers.stripLine(text)

    numberList = []
    # Regex matches all ints
    intList = re.findall(r"(?<!=)(?<!= )(?<!\w)[-+]\d+", strippedText)
    # Regex matches all floats
    floatList = re.findall(r"(?<!=)(?<!= )(?<!\w)[-+]\d+\.\d+(?!\w)", strippedText)
    for i in intList:
        numberList.append(int(i))
    for i in floatList:
        numberList.append(float(i))
    return numberList
