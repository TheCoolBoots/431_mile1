import unittest
import json
from ast_class_definitions import *
from cfgToSSA import topSSACompile
from top_compiler import importMiniFile

class test_cfg_generator(unittest.TestCase):


    def test_phiUnsealed(self):
        ast = importMiniFile('miniFiles/phiUnsealed.mini')
        actual = topSSACompile(ast)
        # expected = ['define i32 @main() {',
        #             'l0:',
        #             'br label %l1',
        #             'l1:',
        #             '%t1 = phi i32 [3, %l0], [%t3, %l2]',
        #             '%t2 = icmp sgt i32 %t1, 10',
        #             'br i1 %t2, label %l2, label %l3',
        #             'l2:',
        #             '%t3 = add i32 %t1, 5',
        #             'br label %l1',
        #             'l3:',
        #             '%t0 = add i32 %t1, 0',
        #             'br label %retLabel',
        #             'retLabel:',
        #             'ret i32 %t1',
        #             '}']


        print('\n'.join(actual))
        # self.assertEqual(actual, expected)

        # print('\n'.join(actual))



if __name__ == '__main__':
    unittest.main()