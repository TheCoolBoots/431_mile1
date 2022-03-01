import unittest
import json
from ast_class_definitions import *
from cfgToSSA import fillPhiPlaceholderLabels, topSSACompile
from top_compiler import importMiniFile

class test_cfg_generator(unittest.TestCase):

    def test_if_oneReturn(self):
        ast = importMiniFile('miniFiles/if_oneReturn.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 1', 
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
                    '%1 = i32 1', 
                    'br i32 %1, label %2, label %3', 
                    '2:', 
                    '%5 = i32 1', 
                    '%0 = i32 %5', 
                    'br label %retLabel', 
                    '3:', 
                    '%6 = i32 3', 
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
                    '%1 = i32 1', 
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
                    '%1 = i32 1', 
                    'br i32 %1, label %2, label %3', '2:', 
                    '%5 = i32 7', 
                    '%6 = call i32 @printf("%d", %5)', 
                    'br label %4', 
                    '3:', 
                    '%7 = i32 5', 
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
                    '%4 = i32 1', 
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
                    '%4 = i32 1', 
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
                    '%7 = phi i32 [%1, %entry], [%6, %4]', 
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
                    '%5 = phi i32 [%9, %3], [%1, %entry]', 
                    '%6 = i32 2', 
                    '%7 = icmp sgt i32 %5, i32 %6', 
                    'br i32 %7, label %3, label %4', 
                    '3:', 
                    '%8 = i32 5', 
                    '%9 = add i32 %5, i32 %8', 
                    'br label %2', 
                    '4:',
                    '%0 = i32 %5',
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']
        self.assertEqual(actual, expected)

        # print('\n'.join(actual))


    def test_phiFilling(self):
        functionCode = ['entry:', 
                    '%1 = i32 3', 
                    '2:', 
                    '%5 = phi i32 [%9, %PLACEHOLDER], [%1, %PLACEHOLDER]', 
                    '3:', 
                    '%8 = i32 5', 
                    '%9 = add i32 %5, i32 %8', ]
        phiIndices = [3]

        expected = ['entry:', 
                    '%1 = i32 3', 
                    '2:', 
                    '%5 = phi i32 [%9, %3], [%1, %entry]', 
                    '3:', 
                    '%8 = i32 5', 
                    '%9 = add i32 %5, i32 %8']

        actual = fillPhiPlaceholderLabels(functionCode, phiIndices)

        self.assertEqual(expected, actual)


    def test_nestedIf(self):
        ast = importMiniFile('miniFiles/nested_if.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {',
                    'entry:',
                    '%1 = i32 1',
                    'br i32 %1, label %2, label %3',
                    '2:',
                    '%5 = i32 1',
                    'br i32 %5, label %6, label %7',
                    '6:',
                    '%9 = i32 4',
                    '%10 = call i32 @printf("%d", %9)',
                    'br label %8',
                    '7:',
                    '%11 = i32 10',
                    '%12 = call i32 @printf("%d", %11)',
                    '8:',
                    'br label %4',
                    '3:',
                    '%13 = i32 13',
                    '%14 = call i32 @printf("%d", %13)',
                    '4:',
                    '%15 = i32 2',
                    '%0 = i32 %15',
                    'br label %retLabel',
                    'retLabel:',
                    'ret i32 %0',
                    '}']

        self.assertEqual(actual, expected)

        # print('\n'.join(actual))





    def test_nestedWhile(self):
        ast = importMiniFile('miniFiles/nested_while.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '1:', 
                    '%4 = i32 1', 
                    'br i32 %4, label %2, label %3', 
                    '2:', 
                    '5:', 
                    '%8 = i32 1', 
                    'br i32 %8, label %6, label %7', 
                    '6:', 
                    '%9 = i32 2', 
                    '%10 = call i32 @printf("%d", %9)', 
                    'br label %5', 
                    '7:', 
                    'br label %1', 
                    '3:', 
                    '%11 = i32 2', 
                    '%0 = i32 %11', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']

        self.assertEqual(actual, expected)

        # print('\n'.join(actual))



    def test_nestedMixed(self):
        ast = importMiniFile('miniFiles/if_while_nested.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @main() {', 
                    'entry:', 
                    '%1 = i32 1', 
                    'br i32 %1, label %2, label %3', 
                    '2:', 
                    '5:', 
                    '%8 = i32 1', 
                    'br i32 %8, label %6, label %7', 
                    '6:', 
                    '%9 = i32 3', 
                    '%10 = call i32 @printf("%d", %9)', 
                    'br label %5', 
                    '7:', 
                    'br label %4', 
                    '3:', 
                    '%11 = i32 2', 
                    '%12 = call i32 @printf("%d", %11)', 
                    '4:', 
                    '%13 = i32 4', 
                    '%0 = i32 %13', 
                    'br label %retLabel', 
                    'retLabel:', 
                    'ret i32 %0', 
                    '}']

        print(actual)

        # self.assertEqual(actual, expected)

# define i32 @main() {        
# entry:
# %1 = i32 1
# br i32 %1, label %2, label %3    
# 2:
# 5:
# %8 = i32 1
# br i32 %8, label %6, label %7    
# 6:
# %9 = i32 3
# %10 = call i32 @printf("%d", %9) 
# br label %5
# 7:
# br label %4
# 3:
# %11 = i32 2
# %12 = call i32 @printf("%d", %11)
# 4:
# retLabel:
# ret i32 %0
# }



    def test_singleInvocation(self):
        ast = importMiniFile('miniFiles/myFunctionCall.mini')
        actual = topSSACompile(ast)
        expected = ['define i32 @foo(i32 %a) {',
                    '%1 = i32 5',
                    '%2 = call i32 @printf("%d", %1)',
                    '%3 = i32 6',
                    '%0 = i32 %3',
                    'br label %retLabel',
                    'retLabel:',
                    'ret i32 %0',
                    '}',
                    'define i32 @main() {',
                    'entry:',
                    '%1 = i32 1',
                    '%2 = call i32 @foo(i32 %1)',
                    '%0 = i32 %2',
                    'br label %retLabel',
                    'retLabel:',
                    'ret i32 %0',
                    '}']

        # print('\n'.join(actual))

        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()