from ast_class_definitions import *
from ssaGenerator import _generateSSA
import unittest
from top_compiler import importMiniFile


class test_ssa_generator(unittest.TestCase):

    def test_basic(self):
        ast = importMiniFile('ssaFormFiles/basic.mini')
        statementList = ast.functions[0].statements

        code, mappings = _generateSSA(statementList)

        print(code)
        print(mappings)
    

if __name__ == '__main__':
    unittest.main()