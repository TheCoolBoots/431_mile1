import unittest
import json
from ast_class_definitions import *
from json_parser import parse
from ssaControlFlow import astToSSA
from top_compiler import importMiniFile

class test_ssaControlFlow(unittest.TestCase):

    # simplest case of if else, print statement in each
    def test1(dotFlag):
        ast = importMiniFile('miniFiles/if_no_else.mini')
        functionList = astToSSA(ast)
        testCFG1 = functionList[-1]
        print("\n".join(testCFG1.ssaCode))
        expected = ['%1 = i32 1',
                    '%2 = i32 1',
                    '%3 = icmp eq i32 %1, i32 %2',
                    'br i32 %1, label %7, label %8',
                    '7:',
                    '%4 = i32 7'
                    'call i32 @printf("%d", %4)',
                    'br label %8',
                    '8:',
                    '%5 = i32 2',
                    '%6 = i32 1',
                    'ret i32 %6']
        # the guard statement of the mini file has 2 predecessor nodes when it should only have 1
    

if __name__ == '__main__':
    unittest.main()