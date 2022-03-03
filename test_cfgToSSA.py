import unittest
import json
from ast_class_definitions import *
from cfgToSSA import topSSACompile
from top_compiler import importMiniFile

class test_cfg_generator(unittest.TestCase):


    def test_phiUnsealed(self):
        ast = importMiniFile('miniFiles/phiUnsealed.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'l1:', 
                    'l2:', 
                    '%t1 = phi i32 [%t3, %l3], [3, %l1]', 
                    '%t2 = icmp sgt i32 %t1, 2', 
                    'br i32 %t2, label %l3, label %l4', 
                    'l3:', 
                    '%t3 = add i32 %t1, 5', 
                    'br label %l2', 
                    'l4:', 
                    '%t0 = add i32 %t1, 0', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %t0', 
                    '}']


        # print(actual)
        self.assertEqual(actual, expected)

        # print('\n'.join(actual))



if __name__ == '__main__':
    unittest.main()