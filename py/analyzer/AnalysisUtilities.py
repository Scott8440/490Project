import py.LineHelpers as LineHelpers
import re


def extractMagicNumbers(self, text):
    strippedText = LineHelpers.removeStrings(text)
    numberList = re.findall(r"\d+", strippedText)
    return numberList

