from distutils.command.build import build
import unittest
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs
from cfgToSSA import addNodeLabelsAndBranches, sealUnsealedBlocks, topSSACompile, topologicalCFGSort, buildLLVM, \
    firstCFGPass


class test_cfg_generator(unittest.TestCase):

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







    def test_fibonacci(self):
        ast = importMiniFile('benchmarks/Fibonacci/Fibonacci.mini')
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




    # global structs
    def test_global_structs(self):
        ast = importMiniFile('miniFiles/globalStruct.mini')
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


        expected = []
        self.assertEqual(actual, expected)






    # local structs
    def test_local_structs(self):
        ast = importMiniFile('miniFiles/localStruct.mini')
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


        expected = []
        self.assertEqual(actual, expected)



    # global variables
    def test_global_variables(self):
        ast = importMiniFile('miniFiles/globalVariables.mini')
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


        expected = []
        self.assertEqual(actual, expected)


    # print
    def test_print(self):
        ast = importMiniFile('miniFiles/printTest.mini')
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


        expected = []
        self.assertEqual(actual, expected)


    # delete
    def test_delete(self):
        ast = importMiniFile('miniFiles/deleteTest.mini')
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


        expected = []
        self.assertEqual(actual, expected)


    # void values - try to do stuff with a void value?
    def test_void(self):
        ast = importMiniFile('miniFiles/voidTest.mini')
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


        expected = []
        self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()