import unittest
import json
from ast_class_definitions import *
from top_compiler import importMiniFile
import test_ast_trees

class test_cfg_generator(unittest.TestCase):

    def test_if_oneReturn(self):
        ast = importMiniFile('miniFiles/if_oneReturn.mini')
        pass

    def test_if_bothReturn(self):
        ast = importMiniFile('miniFiles/if_bothReturn.mini')
        pass

    def test_if_onePass(self):
        ast = importMiniFile('miniFiles/if_onePass.mini')
        pass

    def test_if_bothPass(self):
        ast = importMiniFile('miniFiles/if_bothPass.mini')
        pass

    def test_while_ret(self):
        ast = importMiniFile('miniFiles/while_ret.mini')
        pass

    def test_while_pass(self):
        ast = importMiniFile('miniFiles/while_pass.mini')
        pass

if __name__ == '__main__':
    unittest.main()