import unittest
import json
from ast_class_definitions import *
from cfgToSSA import topSSACompile
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs

class test_cfg_generator(unittest.TestCase):

    def test_simpleIfPhi(self):
        ast = importMiniFile('phiTests/simpleIfPhi.mini')
        cfg = generateProgCFGs(ast)
    
    def test_simpleWhilePhi(self):
        ast = importMiniFile('phiTests/simpleWhilePhi.mini')
        cfg = generateProgCFGs(ast)
        whileExitNode = cfg[0].rootNode.nextNodes[0].nextNodes[1].label
        


if __name__ == '__main__':
    unittest.main()