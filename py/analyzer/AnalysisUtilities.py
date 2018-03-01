import py.LineHelpers as LineHelpers
import re


def extractMagicNumbers(text):
    strippedText = LineHelpers.stripLine(text)
    # REGEX matches all numbers not following an equals sign
    numberList = re.findall(r"(?<!= )(?<!=)\d+", strippedText)
    for i in range(len(numberList)):
        numberList[i] = int(numberList[i])
    return numberList

