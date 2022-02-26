import unittest
import json
from ast_class_definitions import *
from cfgToSSA import topSSACompile
from top_compiler import importMiniFile

class test_cfg_generator(unittest.TestCase):

    def test_if_oneReturn(self):
        ast = importMiniFile('miniFiles/if_oneReturn.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 True', 
                    'br i32 %1, label %2, label %3', 
                    '2:', 
                    '%4 = i32 1', 
                    '%0 = i32 %4', 
                    'br label %retLabel', 
                    '3:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)
        

    def test_if_bothReturn(self):
        ast = importMiniFile('miniFiles/if_bothReturn.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 True', 
                    'br i32 %1, label %2, label %3', 
                    '2:', 
                    '%5 = i32 1', 
                    '%0 = i32 %5', 
                    'br label %retLabel', 
                    '3:', 
                    '%6 = i32 1', 
                    '%0 = i32 %6', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']

        self.assertEqual(actual, expected)


    def test_if_onePass(self):
        ast = importMiniFile('miniFiles/if_onePass.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 True', 
                    'br i32 %1, label %2, label %3', 
                    '2:', 
                    '%4 = i32 7', 
                    '%5 = call i32 @printf("%d", %4)', 
                    '3:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)


    def test_if_bothPass(self):
        ast = importMiniFile('miniFiles/if_bothPass.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 True', 
                    'br i32 %1, label %2, label %3', '2:', 
                    '%5 = i32 7', 
                    '%6 = call i32 @printf("%d", %5)', 
                    'br label %4', 
                    '3:', 
                    '%7 = i32 7', 
                    '%8 = call i32 @printf("%d", %7)', 
                    '4:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']

        self.assertEqual(actual, expected)

    def test_while_ret(self):
        ast = importMiniFile('miniFiles/while_ret.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '1:', 
                    '%4 = i32 True', 
                    'br i32 %4, label %2, label %3', 
                    '2:', 
                    '%5 = i32 1', 
                    '%0 = i32 %5', 
                    'br label %retLabel', 
                    '3:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)
        # print(actual)

    def test_while_pass(self):
        ast = importMiniFile('miniFiles/while_pass.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '1:', 
                    '%4 = i32 True', 
                    'br i32 %4, label %2, label %3', 
                    '2:', 
                    '%5 = i32 5', 
                    '%6 = call i32 @printf("%d", %5)', 
                    'br label %1',
                    '3:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)
        # print('\n'.join(actual))

    def test_phiBasic(self):
        ast = importMiniFile('miniFiles/phiBasic.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 3', 
                    '%2 = i32 2', 
                    '%3 = icmp sgt i32 %1, i32 %2', 
                    'br i32 %3, label %4, label %5', 
                    '4:', 
                    '%6 = i32 5', 
                    '5:', 
                    '%7 = phi(i32 %1, i32 %6)', 
                    '%0 = i32 %7', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)
        # print(actual)


    def test_phiUnsealed(self):
        ast = importMiniFile('miniFiles/phiUnsealed.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 3', 
                    '2:', 
                    '%5 = phi(_)', 
                    '%6 = i32 2', 
                    '%7 = icmp sgt i32 %5, i32 %6', 
                    'br i32 %7, label %3, label %4', 
                    '3:', 
                    '%8 = i32 5', 
                    '%9 = add i32 %5, i32 %8', 
                    'br label %2', 
                    '4:', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()