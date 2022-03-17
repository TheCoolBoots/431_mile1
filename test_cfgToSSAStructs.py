from distutils.command.build import build
import unittest
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs
from cfgToSSA import addNodeLabelsAndBranches, sealUnsealedBlocks, topSSACompile, topologicalCFGSort, buildLLVM, \
    firstCFGPass


class test_cfg_generator(unittest.TestCase):

    # global structs
    def test_global_structs(self):
        ast = importMiniFile('miniFiles/globalStruct.mini')
        cfgs = generateProgCFGs(ast)
        types = ast.getTypes()
        top_env = ast.getTopEnv(False)
        functions = {}
        lastRegUsed = firstCFGPass(cfgs[0], top_env, types, functions)

        sealUnsealedBlocks(lastRegUsed, cfgs[0])

        sortedNodes = topologicalCFGSort(cfgs[0], False)
        for node in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
        actual = buildLLVM(sortedNodes)

        print(actual)


        expected = []
        ['l1:', 
        '%t1 = call i8* @malloc(8)', 
        '%t2 = bitcast i8* %t1 to %struct.A*', 
        'store %struct.A* %t2, %struct.A** @a', 
        '%t3 = call i8* @malloc(8)', 
        '%t4 = bitcast i8* %t3 to %struct.A*', 
        'store %struct.A* %t4, %struct.A** @b', 
        '%t5 = getelementptr %struct.A, %struct.A* @a, i32 0, i32 0', 
        'store i32 1, i32* %t5', 
        '%t6 = getelementptr %struct.A, %struct.A* @b, i32 0, i32 1', 
        'store i32 2, i32* %t6', 
        '%t7 = load %struct.A** @b', 
        'store %struct.A* %t7, %struct.A** @a', 
        '%t8 = getelementptr %struct.A, %struct.A* @a, i32 0, i32 1', 
        '%t9 = load i32, i32* %t8', 
        'ret i32 %t9']
        # self.assertEqual(actual, expected)






    # # local structs
    # def test_local_structs(self):
    #     ast = importMiniFile('miniFiles/localStruct.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTopTypeEnv()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     print(actual)


    #     expected = []
    #     self.assertEqual(actual, expected)



    # # global variables
    # def test_global_variables(self):
    #     ast = importMiniFile('miniFiles/globalVariables.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTopTypeEnv()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     print(actual)


    #     expected = []
    #     self.assertEqual(actual, expected)


    # # print
    # def test_print(self):
    #     ast = importMiniFile('miniFiles/printTest.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTopTypeEnv()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     print(actual)


    #     expected = []
    #     self.assertEqual(actual, expected)


    # # delete
    # def test_delete(self):
    #     ast = importMiniFile('miniFiles/deleteTest.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTopTypeEnv()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     print(actual)


    #     expected = []
    #     self.assertEqual(actual, expected)


    # # void values - try to do stuff with a void value?
    # def test_void(self):
    #     ast = importMiniFile('miniFiles/voidTest.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTopTypeEnv()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], types, top_env, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     print(actual)


    #     expected = []
    #     self.assertEqual(actual, expected)



if __name__ == '__main__':
    unittest.main()