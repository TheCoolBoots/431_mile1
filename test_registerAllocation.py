import unittest
from cfgToSSA import fillPhiPlaceholderLabels, topSSACompile
from top_compiler import importMiniFile


class test_llvmToARM(unittest.TestCase):

    def test_0(self):
        ast = importMiniFile('miniFiles/0.mini')
        actual = cfgToARM(topSSACompile(ast))                   # this will be written by Andrew
        actual = allocateRegisters(actual, numberOfRegisters)   # my function for allocating registers


        expected = [
            'Write register allocated code',
            'in a list'
        ]


        self.assertEqual(actual, expected)