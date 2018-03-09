import unittest
from py.code_rep.CodeBlock import CodeBlock
from py.code_rep.CodeLine import CodeLine

class TestBlockMethods(unittest.TestCase):

    def testBlockCreation(self):
        block = CodeBlock(7, blockType='while')
        self.assertEqual(block.lineNumber, 7)
        self.assertEqual(block.blockType, 'while')
        self.assertEqual(block.lines, [])
        self.assertEqual(block.childrenBlocks, [])
        self.assertEqual(block.lineNumber, 7)

    def testChildBlockAdd(self):
        block = CodeBlock(7, 'while')
        childBlock = CodeBlock(10, blockType='if')
        block.addChildBlock(childBlock)
        self.assertEqual(len(block.childrenBlocks), 1)
        self.assertEqual(block.childrenBlocks[0].lineNumber, 10)
        self.assertEqual(block.childrenBlocks[0].blockType, 'if')

    def testGetLength(self):
        block = CodeBlock(7, blockType='while')
        block.addLine(CodeLine('test line 1', 8, 0))
        block.addLine(CodeLine('test line 2', 9, 0))
        childBlock = CodeBlock(10, 'if')
        childBlock.addLine(CodeLine('child test line 1', 11, 0))
        childBlock.addLine(CodeLine('child test line 2', 12, 0))
        block.addChildBlock(childBlock)
        self.assertEqual(block.getLength(), 4)
    

if __name__ == '__main__':
    unittest.main()
