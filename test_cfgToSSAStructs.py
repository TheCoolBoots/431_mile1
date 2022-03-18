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
    #     actual = topSSACompile(ast)

    #     expected = ['%struct.A = type {i32, i32}', 
    #                 '@a = common dso_local global %struct.A* null', 
    #                 '@b = common dso_local global %struct.A* null', 
    #                 'define i32 @main() {',
    #                 'l1:', 
    #                 '%t1 = call i8* @malloc(i32 8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 'store %struct.A* %t2, %struct.A** @a', 
    #                 '%t3 = call i8* @malloc(i32 8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 'store %struct.A* %t4, %struct.A** @b', 
    #                 '%t5 = getelementptr %struct.A, %struct.A* @a, i32 0, i32 0', 
    #                 'store i32 1, i32* %t5', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* @b, i32 0, i32 1', 
    #                 'store i32 2, i32* %t6', 
    #                 '%t7 = load %struct.A** @b', 
    #                 'store %struct.A* %t7, %struct.A** @a', 
    #                 '%t8 = load %struct.A** @a', 
    #                 '%t9 = getelementptr %struct.A, %struct.A* %t8, i32 0, i32 1', 
    #                 '%t10 = load i32, i32* %t9', 
    #                 'ret i32 %t10', 
    #                 '}']
    #     self.assertEqual(actual, expected)


    # # local structs
    # def test_local_structs(self):
    #     ast = importMiniFile('miniFiles/localStruct.mini')
    #     actual = topSSACompile(ast)

    #     expected = ['%struct.A = type {i32, i32}', 
    #                 'define i32 @main() {', 
    #                 'l1:', 
    #                 '%t1 = call i8* @malloc(i32 8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 '%t3 = call i8* @malloc(i32 8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 '%t5 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 0', 
    #                 'store i32 1, i32* %t5', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* %t4, i32 0, i32 1', 
    #                 'store i32 2, i32* %t6', 
    #                 '%t7 = getelementptr %struct.A, %struct.A* %t4, i32 0, i32 1', 
    #                 '%t8 = load i32, i32* %t7', 
    #                 'ret i32 %t8', 
    #                 '}']

    #     self.assertEqual(actual, expected)

    # def test_nested_structs(self):
    #     ast = importMiniFile('miniFiles/nestedStruct.mini')
    #     actual = topSSACompile(ast)

    #     # print(actual)

    #     expected = ['%struct.A = type {i32, %struct.A*}', 
    #                 'define i32 @main() {', 
    #                 'l1:', 
    #                 '%t1 = call i8* @malloc(i32 8)', 
    #                 '%t2 = bitcast i8* %t1 to %struct.A*', 
    #                 '%t3 = call i8* @malloc(i32 8)', 
    #                 '%t4 = bitcast i8* %t3 to %struct.A*', 
    #                 '%t5 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 'store %struct.A* %t4, %struct.A** %t5', 
    #                 '%t6 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 '%t7 = getelementptr %struct.A, %struct.A* %t6, i32 0, i32 0', 
    #                 'store i32 2, i32* %t7', 
    #                 '%t8 = getelementptr %struct.A, %struct.A* %t2, i32 0, i32 1', 
    #                 '%t9 = getelementptr %struct.A, %struct.A* %t8, i32 0, i32 0', 
    #                 '%t10 = load i32, i32* %t9', 
    #                 'ret i32 %t10', 
    #                 '}']

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
    #     '%t1 = call i8* @malloc(i32 8)', 
    #     '%t2 = bitcast i8* %t1 to %struct.A*', 
    #     '%t3 = call void @deathSort()', 
    #     'ret null', 
    #     '}']
    #     self.assertEqual(expected, actual)

    # def test_primes(self):
    #     ast = importMiniFile('benchmarks/primes/primes.mini')
    #     actual = topSSACompile(ast)

    #     expected = ['define i32 @isqrt(i32 %a) {', 
    #                 'l1:', 
    #                 'br label %l2', 
    #                 'l2:', 
    #                 '%t1 = phi i32 [%t3, %l3], [1, %l1]', 
    #                 '%t2 = phi i32 [%t4, %l3], [3, %l1]', 
    #                 '%t7 = phi i32 [%t7, %l3], [%a, %l1]', 
    #                 '%t8 = icmp sle i32 %t1, %t7', 
    #                 'br i1 %t8, label %l3, label %l4', 
    #                 'l3:', 
    #                 '%t3 = add i32 %t1, %t2', 
    #                 '%t4 = add i32 %t2, 2', 
    #                 'br label %l2', 
    #                 'l4:', 
    #                 '%t5 = div i32 %t2, 2', 
    #                 '%t6 = sub i32 %t5, 1', 
    #                 'ret i32 %t6', 
    #                 '}', 

    #                 'define i1 @prime(i32 %a) {', 
    #                 'l1:', 
    #                 'br label %l2', 
    #                 'l2:', 
    #                 '%t9 = icmp slt i32 %a, 2', 
    #                 'br i1 %t9, label %l3, label %l4', 
    #                 'l3:', 
    #                 'ret i1 0', 
    #                 'l4:', 
    #                 '%t1 = call i32 @isqrt(i32 %a)', 
    #                 'br label %l5', 
    #                 'l5:', 
    #                 # while divisor <= max
    #                 '%t2 = phi i32 [%t2, %l9], [%a, %l4]',  # a
    #                 '%t3 = phi i32 [%t8, %l9], [2, %l4]',   # divisor
    #                 '%t7 = phi i32 [%t6, %l9], [0, %l4]', 
    #                 '%t10 = phi i32 [%t10, %l9], [%t1, %l4]', 
    #                 '%t11 = icmp sle i32 %t3, %t10', 
    #                 'br i1 %t11, label %l6, label %l10', 
    #                 'l6:', 
    #                 '%t4 = div i32 %t2, %t3', 
    #                 '%t5 = mul i32 %t4, %t3', 
    #                 '%t6 = sub i32 %t2, %t5', # remainder
    #                 'br label %l7', 
    #                 'l7:', 
    #                 '%t12 = icmp eq i32 %t6, 0', 
    #                 'br i1 %t12, label %l8, label %l9', 
    #                 'l8:', 
    #                 'ret i1 0', 
    #                 'l9:', 
    #                 '%t8 = add i32 %t3, 1', # divisor
    #                 'br label %l5', 
    #                 'l10:', 
    #                 'ret i1 1', 
    #                 '}', 

    #                 'define i32 @main() {', 
    #                 'l1:', 
    #                 '%t1 = alloca i32', 
    #                 '%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)', 
    #                 '%t3 = load i32, i32* %t1', 
    #                 'br label %l2', 
    #                 'l2:', 
    #                 '%t4 = phi i32 [%t7, %l6], [0, %l1]', 
    #                 '%t8 = phi i32 [%t11, %l6], [%t3, %l1]', 
    #                 '%t9 = icmp sle i32 %t4, %t8', 
    #                 'br i1 %t9, label %l3, label %l7', 
    #                 'l3:', 
    #                 'br label %l4', 
    #                 'l4:', 
    #                 '%t10 = call i1 @prime(i32 %t4)', 
    #                 'br i1 %t10, label %l5, label %l6', 
    #                 'l5:', 
    #                 '%t5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)', 
    #                 'br label %l6', 
    #                 'l6:', 
    #                 '%t11 = phi i32 [%t8, %l4], [%t8, %l5]', '%t6 = phi i32 [%t4, %l4], [%t4, %l5]', 
    #                 '%t7 = add i32 %t6, 1', 
    #                 'br label %l2', 
    #                 'l7:', 
    #                 'ret i32 0', 
    #                 '}']
    #     self.assertEqual(actual, expected)

    def test_mixed(self):
        ast = importMiniFile('benchmarks\mixed\mixed.mini')
        actual = topSSACompile(ast)

    



if __name__ == '__main__':
    unittest.main()