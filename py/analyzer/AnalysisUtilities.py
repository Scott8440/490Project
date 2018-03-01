import py.LineHelpers as LineHelpers
import re


def extractMagicNumbers(text):
    strippedText = LineHelpers.stripLine(text)
    numberList = re.findall(r"\d+", strippedText)
    return numberList

