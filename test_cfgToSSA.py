from distutils.command.build import build
import unittest
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs
from cfgToSSA import addNodeLabelsAndBranches, sealUnsealedBlocks, topSSACompile, topologicalCFGSort, buildLLVM, firstCFGPass

class test_cfg_generator(unittest.TestCase):

    def test_topologicalSort(self):
        ast = importMiniFile('phiTests/simpleWhilePhi.mini')
        cfgs = generateProgCFGs(ast)

        expectedOrder = [1, 2, 3, 4, 0]
        self.assertEqual(expectedOrder, topologicalCFGSort(cfgs[0], True))

    def test_topologicalSort2(self):
        ast = importMiniFile('miniFiles/nested_if.mini')
        functions = generateProgCFGs(ast)
        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {', 
        '  1 -> 2;', 
        '  2 -> 3;', 
        '  2 -> 8;', 
        '  3 -> 4;', 
        '  8 -> 9;', 
        '  4 -> 5;', 
        '  4 -> 6;', 
        '  9 -> 0;', 
        '  5 -> 7;', 
        '  6 -> 7;', 
        '  7 -> 9;', 
        '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node', 
        '2: if guard node', 
        '3: statement block node', 
        '8: statement block node', 
        '4: if guard node', 
        '9: if exit node', 
        '5: statement block node', 
        '6: statement block node', 
        '0: return node', 
        '7: if exit node']
        self.assertEqual(labels, expectedLabels)

        expectedOrder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        self.assertEqual(expectedOrder, topologicalCFGSort(functions[0], True))

    def test_simpleIfPhi(self):
        ast = importMiniFile('phiTests/simpleIfPhi.mini')
        actual = topSSACompile(ast)

        expected = ['define i32 @main() {', 
        'l1:', 
        'br label %l2', 
        'l2:', 
        '%t2 = icmp slt i32 3, 5', 
        'br i1 %t2, label %l3, label %l4', 
        'l3:', 
        'br label %l4', 
        'l4:', 
        '%t1 = phi i32 [3, %l2], [7, %l3]', 
        'ret i32 %t1', 
        '}']

        self.assertEqual(actual, expected)
    
    def test_simpleWhilePhi(self):
        ast = importMiniFile('phiTests/simpleWhilePhi.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTypes()
        top_env = ast.getTopEnv(False)
        functions = {}
        initialMappings = cfgs[0].ast.getSSALocalMappings()
        cfgs[0].rootNode.mappings = initialMappings
        
        # print(whileExitNode.llvmCode)
        sortedNodes = topologicalCFGSort(cfgs[0], False)
        lastRegUsed = firstCFGPass(sortedNodes, types, top_env, functions)

        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        expected = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '1-2-x-*', 
                    '%t3 = icmp slt i32 %t1, 5', 
                    'br i1 %t3, label %l3, label %l4', 
                    'l3:', 
                    '%t2 = add i32 %t1, 1', 
                    'br label %l2', 
                    'l4:', 
                    'ret i32 %t1']

        self.assertEqual(actual, expected)

    def test_complexWhilePhi(self):
        ast = importMiniFile('phiTests/complexWhilePhi.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}
        initialMappings = cfgs[0].ast.getSSALocalMappings()
        cfgs[0].rootNode.mappings = initialMappings
        sortedNodes = topologicalCFGSort(cfgs[0], False)
        lastRegUsed = firstCFGPass(sortedNodes, types, top_env, functions)

        # print(whileExitNode.llvmCode)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        expected = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '1-2-x-*', 
                    '3-2-y-*', 
                    '%t5 = icmp slt i32 %t1, 5', 
                    'br i1 %t5, label %l3, label %l4', 
                    'l3:', 
                    '%t2 = add i32 %t1, 1', 
                    '%t4 = add i32 %t3, 3', 
                    'br label %l2', 
                    'l4:', 
                    'ret i32 %t3']
        self.assertEqual(actual, expected)

        sealUnsealedBlocks(lastRegUsed, cfgs[0])
        actual2 = buildLLVM(sortedNodes)

        expected2 = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '%t1 = phi i32 [%t2, %l3], [3, %l1]', 
                    '%t3 = phi i32 [%t4, %l3], [2, %l1]', 
                    '%t5 = icmp slt i32 %t1, 5', 
                    'br i1 %t5, label %l3, label %l4', 
                    'l3:', 
                    '%t2 = add i32 %t1, 1', 
                    '%t4 = add i32 %t3, 3', 
                    'br label %l2', 
                    'l4:', 
                    'ret i32 %t3']

        self.assertEqual(actual2, expected2)

    def test_analysis1(self):
        ast = importMiniFile('analysisFiles/analysis1.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}

        initialMappings = cfgs[0].ast.getSSALocalMappings()
        cfgs[0].rootNode.mappings = initialMappings
        sortedNodes = topologicalCFGSort(cfgs[0], False)
        lastRegUsed = firstCFGPass(sortedNodes, types, top_env, functions)

        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)


        lastRegUsed = sealUnsealedBlocks(lastRegUsed, cfgs[0])
        actual = buildLLVM(sortedNodes)
        
        expected = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '%t1 = phi i32 [%t9, %l10], [0, %l1]', # val1
                    '%t3 = phi i32 [%t10, %l10], [0, %l1]', # val2
                    '%t5 = phi i32 [%t7, %l10], [0, %l1]',  # check
                    'br i1 1, label %l3, label %l11', 
                    # while loop
                    'l3:', 
                    'br label %l4', 
                    'l4:', 
                    # if guard
                    'br i1 1, label %l5, label %l6', 
                    'l5:', 
                    '%t2 = add i32 %t1, 1', 
                    'br label %l7', 
                    'l6:', 
                    # if else
                    '%t4 = add i32 %t3, 1', 
                    'br label %l7', 
                    'l7:', 
                    '%t10 = phi i32 [%t3, %l5], [%t4, %l6]',  # val2
                    '%t9 = phi i32 [%t2, %l5], [%t1, %l6]',  # val1
                    '%t6 = phi i32 [%t5, %l5], [%t5, %l6]',  # check
                    '%t7 = add i32 %t6, 1', 
                    'br label %l8', 
                    'l8:', 
                    '%t8 = icmp sgt i32 %t7, 90000', 
                    'br i1 %t8, label %l9, label %l10', 
                    'l9:', 
                    'ret i32 %t7', 
                    'l10:', 
                    'br label %l2', 
                    # while exit
                    'l11:', 
                    'ret i32 %t5']

        self.assertEqual(actual, expected)

    def test_fibonacciTop(self):
        ast = importMiniFile('benchmarks\Fibonacci\Fibonacci.mini')
        actual = topSSACompile(ast)

        expected = ['define i32 @computeFib(i32 %input) {', 
                    'l1:', 
                    'br label %l2', 
                    'l2:', 
                    '%t6 = icmp eq i32 %input, 0', 
                    'br i1 %t6, label %l3, label %l4', 
                    'l3:', 
                    'ret i32 0', 
                    'l4:', 
                    'br label %l5', 
                    'l5:', 
                    '%t7 = icmp sle i32 %input, 2', 
                    'br i1 %t7, label %l6, label %l7', 
                    'l6:', 
                    'ret i32 1', 
                    'l7:', 
                    '%t1 = sub i32 %input, 1', 
                    '%t2 = call i32 @computeFib(i32 %t1)', 
                    '%t3 = sub i32 %input, 2', 
                    '%t4 = call i32 @computeFib(i32 %t3)', 
                    '%t5 = add i32 %t2, %t4', 
                    'ret i32 %t5', 
                    '}', 
                    'define i32 @main() {', 
                    'l1:', 
                    '%t1 = alloca i32', 
                    '%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)', 
                    '%t3 = load i32, i32* %t1', 
                    '%t4 = call i32 @computeFib(i32 %t3)', 
                    '%t5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)', 
                    'ret i32 0', 
                    '}']
        self.assertEqual(actual, expected)
        # print(actual)

    def test_booleans(self):
        ast = importMiniFile('phiTests/bools.mini')
        actual = topSSACompile(ast)
        print(actual)
        expected = ['define i1 @boolean() {', 
                    'l1:', 
                    'br label %l2', 
                    'l2:', 
                    'br i1 1, label %l3, label %l4', 
                    'l3:', 
                    'ret i1 0', 
                    'l4:', 
                    'ret i1 1', 
                    '}', 
                    'define i32 @main() {', 
                    'l1:', 
                    '%t1 = call i1 @boolean()', 
                    'ret i1 %t1', 
                    '}']


if __name__ == '__main__':
    unittest.main()