import unittest
from py.analyzer.MagicNumberAlert import MagicNumberAlert

class TestMagicNumberAlert(unittest.TestCase):

    def testAlertCreation(self):
        alert = MagicNumberAlert(23, 10)
        self.assertEqual(alert.alertType, "Magic Number")
        self.assertEqual(alert.number, 23)
        self.assertEqual(alert.lineNumber, 10)
        correctDescription = "There is a 'magic number' 23 line 10"
        self.assertEqual(alert.alertDescription, correctDescription)
        correctFixText = ("You should consider setting this number to be "
                          "a named constant and replacing all occurences of "
                          "the number with this constant.")
        self.assertEqual(alert.fixText, correctFixText)

if __name__ == '__main__':
    unittest.main()
