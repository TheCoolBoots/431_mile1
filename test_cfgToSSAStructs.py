from distutils.command.build import build
import unittest
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs
from cfgToSSA import addNodeLabelsAndBranches, sealUnsealedBlocks, topSSACompile, topologicalCFGSort, buildLLVM, \
    firstCFGPass


class test_cfg_generator(unittest.TestCase):

    # def test_global_structs(self):
    #     ast = importMiniFile('miniFiles/globalStruct.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTypes()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], top_env, types, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     expected = ['l1:', 
    #                 '%t1 = call i8* @malloc(8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 'store %struct.A* %t2, %struct.A** @a', 
    #                 '%t3 = call i8* @malloc(8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 'store %struct.A* %t4, %struct.A** @b', 
    #                 '%t5 = load %struct.A** @a', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* %t5, i32 0, i32 0', 
    #                 'store i32 1, i32* %t6', 
    #                 '%t7 = load %struct.A** @b', 
    #                 '%t8 = getelementptr %struct.A, %struct.A* %t7, i32 0, i32 1', 
    #                 'store i32 2, i32* %t8', 
    #                 '%t9 = load %struct.A** @b', 
    #                 'store %struct.A* %t9, %struct.A** @a', 
    #                 '%t10 = load %struct.A** @a', 
    #                 '%t11 = getelementptr %struct.A, %struct.A* %t10, i32 0, i32 1', 
    #                 '%t12 = load i32, i32* %t11', 
    #                 'ret i32 %t12']
    #     self.assertEqual(actual, expected)


    # # local structs
    # def test_local_structs(self):
    #     ast = importMiniFile('miniFiles/localStruct.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTypes()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], top_env, types, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     expected = ['l1:', 
    #                 '%t1 = call i8* @malloc(8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 '%t3 = call i8* @malloc(8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 '%t5 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 0', 
    #                 'store i32 1, i32* %t5', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* %t4, i32 0, i32 1', 
    #                 'store i32 2, i32* %t6', 
    #                 '%t7 = getelementptr %struct.A, %struct.A* %t4, i32 0, i32 1', 
    #                 '%t8 = load i32, i32* %t7', 
    #                 'ret i32 %t8']

    #     self.assertEqual(actual, expected)


    # # global variables
    # def test_nested_structs(self):
    #     ast = importMiniFile('miniFiles/nestedStruct.mini')
    #     cfgs = generateProgCFGs(ast)
    #     types = ast.getTypes()
    #     top_env = ast.getTopEnv(False)
    #     functions = {}
    #     lastRegUsed = firstCFGPass(cfgs[0], top_env, types, functions)

    #     sealUnsealedBlocks(lastRegUsed, cfgs[0])

    #     sortedNodes = topologicalCFGSort(cfgs[0], False)
    #     for node in sortedNodes:
    #         lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, node, top_env, types, functions)
    #     actual = buildLLVM(sortedNodes)

    #     expected = ['l1:', 
    #                 '%t1 = call i8* @malloc(8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 '%t3 = call i8* @malloc(8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 '%t5 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 'store %struct.A* %t4, %struct.A** %t5', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 '%t7 = getelementptr %struct.A, %struct.A* 6, i32 0, i32 0', 
    #                 'store i32 2, i32* %t7', 
    #                 '%t8 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 '%t9 = getelementptr %struct.A, %struct.A* %t8, i32 0, i32 0', 
    #                 '%t10 = load i32, i32* %t9', 
    #                 'ret i32 %t10']

    #     self.assertEqual(actual, expected)


    # # void values - try to do stuff with a void value?
    # def test_void(self):
    #     ast = importMiniFile('miniFiles/voidTest.mini')
    #     # ast = importMiniFile("benchmarks/killerBubbles/killerBubbles.mini")
    #     actual = topSSACompile(ast)

    #     expected = ['%struct.A = type {i32, i32}', 
    #     'define void @deathSort() {', 
    #     'l1:', 
    #     'ret null', 
    #     '}', 
    #     'define i32 @main() {', 
    #     'l1:', 
    #     '%t1 = call i8* @malloc(8)', 
    #     '%t2 = bitcast i8* %t1 to %struct.A*', 
    #     '%t3 = call void @deathSort()', 
    #     'ret null', 
    #     '}']
    #     self.assertEqual(expected, actual)

    # def test_stats(self):
    #     ast = importMiniFile('benchmarks\stats\stats.mini')
    #     actual = topSSACompile(ast)

    #     print(actual)

    



if __name__ == '__main__':
    unittest.main()