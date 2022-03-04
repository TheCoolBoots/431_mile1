
import unittest

class test_llvmToARM(unittest.TestCase):
    def test_phiIf(self):
        with open('llvmToARMFiles/phiIf.ll') as inputFile:
            input = inputFile.read()
        input = input.split('\n')


    def test_phiIfElse(self):
        with open('llvmToARMFiles/phiIf.ll') as inputFile:
            input = inputFile.read()
        input = input.split('\n')


    def test_phiWhile(self):
        with open('llvmToARMFiles/phiIf.ll') as inputFile:
            input = inputFile.read()
        input = input.split('\n')