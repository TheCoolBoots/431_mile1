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
                    'l0:',
                    'br label %l1',
                    'l1:',
                    '%t1 = phi i32 [%t3, %l2], [3, %l0]',
                    '%t2 = icmp sgt i32 %t1, 10',
                    'br i1 %t2, label %l2, label %l3',
                    'l2:',
                    '%t3 = add i32 %t1, 5',
                    'br label %l1',
                    'l3:',
                    '%t0 = add i32 %t1, 0',
                    'br label %retLabel',
                    'retLabel:',
                    'ret i32 %t0',
                    '}']


        # print('\n'.join(actual))
        self.assertEqual(actual, expected)

        # print('\n'.join(actual))

    def test_phi2(self):
        ast = importMiniFile('analysisFiles/analysis1.mini')
        actual = topSSACompile(ast)

        expected = ['define i32 @main() {', 
                    'l0:', 
                    'br label %l1', 
                    'l1:', 
                    '%t1 = phi i32 [%t9, %l6], [0, %l0]', 
                    '%t2 = icmp slt i32 %t1, 100000', 
                    'br i1 %t2, label %l2, label %l7', 
                    'l2:', 
                    '%t3 = icmp slt i32 %t1, 50000', 
                    'br i1 %t3, label %l4, label %l5', 
                    'l4:', 
                    '%t4 = phi i32 [%t4, %l6], [0, %l0]', 
                    '%t5 = add i32 %t4, 1', 
                    'br label %l6', 
                    'l5:', 
                    '%t6 = phi i32 [%t6, %l6], [0, %l0]', 
                    '%t7 = add i32 %t6, 1', 
                    'br label %l6', 
                    'l6:', 
                    '%t8 = phi i32 [%t1, %l1], [%t1, %l1]', 
                    '%t9 = add i32 %t8, 1', 
                    'br label %l1', 
                    'l7:', 
                    '%t0 = add i32 %t1, 0', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %t0', 
                    '}']

        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()