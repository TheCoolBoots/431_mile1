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
        '%t0 = add i32 %t1, 0', 
        'br label %l0', 
        'l0:', 
        'ret i32 %t0', 
        '}']

        self.assertEqual(actual, expected)
    
    def test_simpleWhilePhi(self):
        ast = importMiniFile('phiTests/simpleWhilePhi.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}
        lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)
        whileExitNode = cfgs[0].rootNode.nextNodes[0].nextNodes[1]

        # print(whileExitNode.llvmCode)
        sortedNodes = topologicalCFGSort(cfgs[0], False)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        expected = ['l1:', 
            'br label %l2', 
            'l2:', 
            '1-2-x-*', 
            '%t2 = icmp slt i32 %t1, 5', 
            'br i1 %t2, label %l3, label %l4', 
            'l3:', 
            '%t2 = add i32 %t1, 1', 
            'br label %l2', 
            'l4:', 
            '%t0 = add i32 %t1, 0', 
            'br label %l0', 
            'l0:']

        self.assertEqual(actual, expected)

    def test_complexWhilePhi(self):
        ast = importMiniFile('phiTests/complexWhilePhi.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}
        lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

        # print(whileExitNode.llvmCode)
        sortedNodes = topologicalCFGSort(cfgs[0], False)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        expected = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '1-2-x-*', 
                    '3-2-y-*', 
                    '%t4 = icmp slt i32 %t1, 5', 
                    'br i1 %t4, label %l3, label %l4', 
                    'l3:', 
                    '%t2 = add i32 %t1, 1', 
                    '%t4 = add i32 %t3, 3', 
                    'br label %l2', 
                    'l4:', 
                    '%t0 = add i32 %t3, 0', 
                    'br label %l0', 
                    'l0:']
        self.assertEqual(actual, expected)

        sealUnsealedBlocks(lastRegUsed, cfgs[0])
        actual2 = buildLLVM(sortedNodes)

        expected2 = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '%t1 = phi i32 [%t2, %l3], [3, %l1]', 
                    '%t3 = phi i32 [%t4, %l3], [2, %l1]', 
                    '%t4 = icmp slt i32 %t1, 5', 
                    'br i1 %t4, label %l3, label %l4', 
                    'l3:', 
                    '%t2 = add i32 %t1, 1', 
                    '%t4 = add i32 %t3, 3', 
                    'br label %l2', 
                    'l4:', 
                    '%t0 = add i32 %t3, 0', 
                    'br label %l0', 
                    'l0:']

        self.assertEqual(actual2, expected2)

    def test_analysis1(self):
        ast = importMiniFile('analysisFiles/analysis1.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}
        lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

        sealUnsealedBlocks(lastRegUsed, cfgs[0])

        sortedNodes = topologicalCFGSort(cfgs[0], False)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)
        
        expected = ['l1:', 
                    'br label %l2', 
                    'l2:', 
                    '%t1 = phi i32 [%t7, %l10], [0, %l1]', 
                    '%t2 = phi i32 [%t8, %l10], [0, %l1]', 
                    '%t4 = phi i32 [%t9, %l10], [0, %l1]', 
                    'br i1 1, label %l3, label %l11', 
                    'l3:', 
                    'br label %l4', 
                    'l4:', 
                    'br i1 1, label %l5, label %l6', 
                    'l5:', 
                    '%t3 = add i32 %t2, 1', 
                    'br label %l7', 
                    'l6:', 
                    '%t5 = add i32 %t4, 1', 
                    'br label %l7', 
                    'l7:', 
                    '%t9 = phi i32 [%t4, %l5], [%t5, %l6]', 
                    '%t8 = phi i32 [%t3, %l5], [%t2, %l6]', 
                    '%t6 = phi i32 [%t1, %l5], [%t1, %l6]', 
                    '%t7 = add i32 %t6, 1', 
                    'br label %l8', 
                    'l8:', 
                    '%t8 = icmp sgt i32 %t7, 90000', 
                    'br i1 %t8, label %l9, label %l10', 
                    'l9:', 
                    '%t0 = add i32 %t7, 0', 
                    'br label %l0', 
                    'l10:', 
                    'br label %l2', 
                    'l11:', 
                    '%t0 = add i32 %t1, 0', 
                    'br label %l0', 
                    'l0:']

        self.assertEqual(actual, expected)

    def test_fibonacci(self):
        ast = importMiniFile('benchmarks\Fibonacci\Fibonacci.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTopTypeEnv()
        top_env = ast.getTopEnv(False)
        functions = {}
        lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

        sealUnsealedBlocks(lastRegUsed, cfgs[0])

        sortedNodes = topologicalCFGSort(cfgs[0], False)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        print(actual)
        


if __name__ == '__main__':
    unittest.main()