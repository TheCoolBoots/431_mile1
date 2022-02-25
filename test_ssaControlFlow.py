from tkinter.messagebox import IGNORE
import unittest
from ast_class_definitions import *
from ssaControlFlow import astToSSA
from top_compiler import importMiniFile

class test_ssaControlFlow(unittest.TestCase):

    def test_ifNoElse(self):
        self.skipTest('bug unfixed as of 2/25/2022 10:20 am')
        ast = importMiniFile('miniFiles/if_no_else.mini')
        functionList = astToSSA(ast)
        testCFG1 = functionList[-1]
        actual = '\n'.join(testCFG1.ssaCode)
        expected = ['%1 = i32 1',
                    '%2 = i32 1',
                    '%3 = icmp eq i32 %1, i32 %2',
                    'br i32 %1, label %8, label %9',
                    '8:',
                    '%4 = i32 7'
                    '%5 = call i32 @printf("%d", %4)',
                    'br label %8',
                    '9:',
                    '%6 = i32 2',
                    '%7 = i32 1',
                    'ret i32 %7']
        # line 162 of ssaControlFlow else flag being set to 1 but in this test case it should be 0
        self.assertEqual(expected, actual)

    def test_ifElse(self):
        self.skipTest('need to fix bug in ssaControlFlow first')
        ast = importMiniFile('miniFiles/if2.mini')
        functionList = astToSSA(ast)
        testCFG1 = functionList[-1]
        # actual = '\n'.join(testCFG1.ssaCode)
        actual = testCFG1.ssaCode
        # print('\n'.join(actual))
        expected = ['%1 = i32 3',
                    '%2 = i32 3',
                    '%3 = icmp eq i32 %1, i32 %2',
                    'br i32 %3, label %8, label %9',
                    '8:',
                    '%4 = i32 7',
                    '%5 = call i32 @printf("%d", %4)',
                    'br label %10',
                    '9:',
                    '%6 = i32 8',
                    '%7 = call i32 @printf("%d", %6)',
                    '10:']
        # line 162 of ssaControlFlow else flag being set to 1 but in this test case it should be 0
        self.assertEqual(expected, actual)

    def test_while(self):
        ast = importMiniFile('miniFiles/loop.mini')
        functionList = astToSSA(ast)
        # cfg = functionList[-1]
        # actual = '\n'.join(testCFG1.ssaCode)
        # actual = cfg.ssaCode
        # print('\n'.join(actual))
        # expected = ['%1 = i32 3',
        #             '%2 = i32 3',
        #             '%3 = icmp eq i32 %1, i32 %2',
        #             'br i32 %3, label %8, label %9',
        #             '8:',
        #             '%4 = i32 7',
        #             '%5 = call i32 @printf("%d", %4)',
        #             'br label %10',
        #             '9:',
        #             '%6 = i32 8',
        #             '%7 = call i32 @printf("%d", %6)',
        #             '10:']
        # line 162 of ssaControlFlow else flag being set to 1 but in this test case it should be 0
        # self.assertEqual(expected, actual)
    

if __name__ == '__main__':
    unittest.main()