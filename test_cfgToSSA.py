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

#         # print('\n'.join(actual))


# # NOT WORKING
#     def test_phi2(self):
#         ast = importMiniFile('analysisFiles/analysis1.mini')
#         actual = topSSACompile(ast)

#         """define i32 @main() {
#             l0:
#             br label %l1
#             l1:
#             br i1 1, label %l2, label %l10
#             l2:
#             br i1 1, label %l4, label %l5
#             l4:
#             %t1 = phi i32 [%t2, %l6], [0, %l0]
#             %t2 = add i32 %t1, 1
#             br label %l6
#             l5:
#             %t3 = phi i32 [%t4, %l6], [0, %l0]
#             %t4 = add i32 %t3, 1
#             br label %l6
#             l6:
#             %t5 = phi i32 [5, %l2], [%t5, %l2]
#             %t6 = add i32 %t5, 1
#             %t7 = icmp sgt i32 %t6, 90000
#             br i1 %t7, label %l8, label %l9
#             l8:
#             %t0 = add i32 %t6, 0
#             br label %retLabel
#             l9:
#             br label %l1
#             l10:
#             %t7 = phi i32 [%t6, %l9], [0, %l0]
#             %t0 = add i32 %t7, 0
#             br label %retLabel
#             retLabel:
#             ret i32 %t0
#             }"""
#         print('\n'.join(actual))



    def test_modifyInternal(self):
        ast = importMiniFile('miniFiles/modifyInternal.mini')
        actual = topSSACompile(ast)

        expected = ['define i32 @main() {',
                'l0:',
                '%t1 = add i32 2, 3',
                'br i1 1, label %l2, label %l3',
                'l2:',
                '%t2 = mul i32 %t1, 2',
                '%t3 = add i32 %t1, 1',
                'br label %l8',
                'l3:',
                'br i1 1, label %l5, label %l6',
                'l5:',
                '%t4 = mul i32 2, 9',
                'br label %l7',
                'l6:',
                '%t5 = add i32 %t1, 2',
                'br label %l7',
                'l7:',
                't6 = phi i32 [%t1, %l6], [%t4, %l5]'
                'br label %l8',
                'l8:',
                '%t7 = phi i32 [%t3, %l2], [%t6, %l7]',
                '%t7 = add i32 %t6, 7',
                '%t0 = add i32 %t7, 0',
                'br label %retLabel',
                'retLabel:',
                'ret i32 %t0',
                '}']

        # print('\n'.join(actual))
        # print(actual)

        self.assertEqual(actual, expected)

# BROKEN
    # def test_modifyInternal2(self):
    #     ast = importMiniFile('miniFiles/modifyInternal2.mini')
    #     actual = topSSACompile(ast)

    #     expected_old = ['define i32 @main() {', 
    #     'l0:', 
    #     'br label %l1', 
    #     'l1:', 
    #     '%t1 = phi i32 [%t5, %l2], [0, %l0]', 
    #     '%t2 = icmp slt i32 %t1, 50', 
    #     'br i1 %t2, label %l2, label %l3', 
    #     'l2:', 
    #     '%t3 = phi i32 [%t4, %l2], [0, %l0]', 
    #     '%t4 = add i32 %t3, 1', 
    #     '%t5 = add i32 %t1, 2', 
    #     'br label %l1', 
    #     'l3:', 
    #     '%t6 = phi i32 [%t4, %l2], [0, %l0]', 
    #     '%t0 = add i32 %t6, 0', 
    #     'br label %retLabel', 
    #     'retLabel:', 
    #     'ret i32 %t0', 
    #     '}']

        
    #     expected = ['define i32 @main() {',
    #     'l0:',
    #     'br label %l1',
    #     'l1:',
    #     '%t1 = phi i32 [%t5, %l2], [0, %l0]',
    #     '%t2 = phi i32 [%t4, %l2], [0, %l0]',
    #     '%t3 = icmp slt i32 %t1, 50',
    #     'br i1 %t3, label %l2, label %l3',
    #     'l2:',
    #     '%t4 = add i32 %t2, 1',
    #     '%t5 = add i32 %t1, 2',
    #     'br label %l1',
    #     'l3:',
    #     '%t0 = add i32 %t2, 0',
    #     'br label %retLabel',
    #     'retLabel:',
    #     'ret i32 %t0',
    #     '}']
        

    #     self.assertEqual(actual, expected)
        # print('\n'.join(actual))

    
    def test_nestedIf(self):
        ast = importMiniFile('miniFiles/nestedIf.mini')
        actual = topSSACompile(ast)
        print('\n'.join(actual))



if __name__ == '__main__':
    unittest.main()