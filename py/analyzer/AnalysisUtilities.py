import py.parser.LineHelpers as LineHelpers
import re


def extractMagicNumbers(text):
    strippedText = LineHelpers.stripLine(text)
    # REGEX matches all numbers not following an equals sign or within a word
    numberList = re.findall(r"(?<!= )(?<!=)(?<!\w)\d+(?!\w)", strippedText)
    for i in range(len(numberList)):
        numberList[i] = int(numberList[i])
    return numberList

