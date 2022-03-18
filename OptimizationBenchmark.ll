target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
@global1 = common dso_local global i32 0
@global2 = common dso_local global i32 0
@global3 = common dso_local global i32 0
define i32 @constantFolding() {
l1:
%t1 = mul i32 8, 9
%t2 = sdiv i32 %t1, 4
%t3 = add i32 %t2, 2
%t4 = mul i32 5, 8
%t5 = sub i32 %t3, %t4
%t6 = add i32 %t5, 9
%t7 = sub i32 %t6, 12
%t8 = add i32 %t7, 6
%t9 = sub i32 %t8, 9
%t10 = sub i32 %t9, 18
%t11 = mul i32 23, 3
%t12 = sdiv i32 %t11, 23
%t13 = mul i32 %t12, 90
%t14 = add i32 %t10, %t13
ret i32 %t14
}
define i32 @constantPropagation() {
l1:
%t1 = add i32 4, 7
%t2 = add i32 8, 5
%t3 = add i32 11, 21
%t4 = add i32 %t1, %t2
%t5 = mul i32 %t3, %t4
%t6 = mul i32 %t2, %t3
%t7 = add i32 11, %t6
%t8 = sub i32 %t7, %t5
%t9 = mul i32 %t3, %t4
%t10 = sub i32 %t2, %t9
%t11 = sdiv i32 %t5, %t8
%t12 = add i32 %t10, %t11
%t13 = add i32 11, 21
%t14 = add i32 %t13, %t1
%t15 = add i32 %t14, %t2
%t16 = add i32 %t15, %t3
%t17 = sub i32 %t16, %t4
%t18 = sub i32 %t17, %t12
%t19 = add i32 %t18, %t2
%t20 = sub i32 %t19, 4
%t21 = sub i32 %t20, 7
%t22 = add i32 %t5, %t8
%t23 = sub i32 %t22, %t1
%t24 = sub i32 %t23, %t2
%t25 = sub i32 7, 4
%t26 = mul i32 %t25, 5
%t27 = sub i32 %t26, %t3
%t28 = mul i32 %t8, 8
%t29 = mul i32 %t28, 5
%t30 = add i32 %t29, %t21
%t31 = mul i32 7, 4
%t32 = mul i32 %t31, 8
%t33 = sdiv i32 %t32, 11
%t34 = sub i32 %t33, %t21
%t35 = add i32 %t3, %t5
%t36 = add i32 %t35, 8
%t37 = sub i32 %t36, %t24
%t38 = add i32 %t17, %t21
%t39 = mul i32 21, 4
%t40 = sub i32 %t38, %t39
%t41 = mul i32 4, 7
%t42 = sub i32 %t41, %t5
%t43 = sub i32 %t42, %t8
%t44 = sub i32 %t43, %t34
%t45 = mul i32 %t30, 5
%t46 = sub i32 %t44, %t45
%t47 = sub i32 %t21, %t46
%t48 = sub i32 %t47, %t43
%t49 = sub i32 %t48, %t17
%t50 = mul i32 %t24, %t49
%t51 = add i32 %t50, %t37
%t52 = sub i32 %t51, %t46
%t53 = sub i32 %t46, %t49
%t54 = add i32 %t53, %t52
%t55 = add i32 %t54, %t5
ret i32 %t55
}
define i32 @deadCodeElimination() {
l1:
store i32 11, i32* @global1
store i32 5, i32* @global1
store i32 9, i32* @global1
%t1 = add i32 8, 8
%t2 = add i32 %t1, 9
%t3 = add i32 %t2, 3
%t4 = add i32 %t3, 10
ret i32 %t4
}
define i32 @sum(i32 %number) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t3, %l3], [0, %l1]
%t2 = phi i32 [%t4, %l3], [%number, %l1]
%t5 = icmp sgt i32 %t2, 0
br i1 %t5, label %l3, label %l4
l3:
%t3 = add i32 %t1, %t2
%t4 = sub i32 %t2, 1
br label %l2
l4:
ret i32 %t1
}
define i32 @doesntModifyGlobals() {
l1:
%t1 = add i32 1, 2
ret i32 %t1
}
define i32 @interProceduralOptimization() {
l1:
store i32 1, i32* @global1
store i32 0, i32* @global2
store i32 0, i32* @global3
%t1 = call i32 @sum(i32 100)
br label %l2
l2:
%t8 = load i32, i32* @global1
%t9 = icmp eq i32 %t8, 1
br i1 %t9, label %l3, label %l4
l3:
%t2 = call i32 @sum(i32 10000)
br label %l11
l4:
br label %l5
l5:
%t10 = load i32, i32* @global2
%t11 = icmp eq i32 %t10, 2
br i1 %t11, label %l6, label %l7
l6:
%t3 = call i32 @sum(i32 20000)
br label %l7
l7:
%t5 = phi i32 [%t1, %l5], [%t3, %l6]
br label %l8
l8:
%t12 = load i32, i32* @global3
%t13 = icmp eq i32 %t12, 3
br i1 %t13, label %l9, label %l10
l9:
%t4 = call i32 @sum(i32 30000)
br label %l10
l10:
%t6 = phi i32 [%t5, %l8], [%t4, %l9]
br label %l11
l11:
%t7 = phi i32 [%t2, %l3], [%t6, %l10]
ret i32 %t7
}
define i32 @commonSubexpressionElimination() {
l1:
%t1 = mul i32 11, 22
%t2 = sdiv i32 33, 44
%t3 = mul i32 55, 66
%t4 = mul i32 11, 22
%t5 = sdiv i32 33, 44
%t6 = add i32 %t4, %t5
%t7 = mul i32 55, 66
%t8 = sub i32 %t6, %t7
%t9 = add i32 %t8, 77
%t10 = mul i32 11, 22
%t11 = sdiv i32 33, 44
%t12 = add i32 %t10, %t11
%t13 = mul i32 55, 66
%t14 = sub i32 %t12, %t13
%t15 = add i32 %t14, 77
%t16 = mul i32 11, 22
%t17 = sdiv i32 33, 44
%t18 = add i32 %t16, %t17
%t19 = mul i32 55, 66
%t20 = sub i32 %t18, %t19
%t21 = add i32 %t20, 77
%t22 = mul i32 11, 22
%t23 = sdiv i32 33, 44
%t24 = add i32 %t22, %t23
%t25 = mul i32 55, 66
%t26 = sub i32 %t24, %t25
%t27 = add i32 %t26, 77
%t28 = mul i32 11, 22
%t29 = sdiv i32 33, 44
%t30 = add i32 %t28, %t29
%t31 = mul i32 55, 66
%t32 = sub i32 %t30, %t31
%t33 = add i32 %t32, 77
%t34 = mul i32 11, 22
%t35 = sdiv i32 33, 44
%t36 = add i32 %t34, %t35
%t37 = mul i32 55, 66
%t38 = sub i32 %t36, %t37
%t39 = add i32 %t38, 77
%t40 = mul i32 11, 22
%t41 = sdiv i32 33, 44
%t42 = add i32 %t40, %t41
%t43 = mul i32 55, 66
%t44 = sub i32 %t42, %t43
%t45 = add i32 %t44, 77
%t46 = mul i32 11, 22
%t47 = sdiv i32 33, 44
%t48 = add i32 %t46, %t47
%t49 = mul i32 55, 66
%t50 = sub i32 %t48, %t49
%t51 = add i32 %t50, 77
%t52 = mul i32 11, 22
%t53 = sdiv i32 33, 44
%t54 = add i32 %t52, %t53
%t55 = mul i32 55, 66
%t56 = sub i32 %t54, %t55
%t57 = add i32 %t56, 77
%t58 = mul i32 11, 22
%t59 = sdiv i32 33, 44
%t60 = add i32 %t58, %t59
%t61 = mul i32 55, 66
%t62 = sub i32 %t60, %t61
%t63 = add i32 %t62, 77
%t64 = mul i32 11, 22
%t65 = sdiv i32 33, 44
%t66 = add i32 %t64, %t65
%t67 = mul i32 55, 66
%t68 = sub i32 %t66, %t67
%t69 = add i32 %t68, 77
%t70 = mul i32 22, 11
%t71 = sdiv i32 33, 44
%t72 = add i32 %t70, %t71
%t73 = mul i32 55, 66
%t74 = sub i32 %t72, %t73
%t75 = add i32 %t74, 77
%t76 = mul i32 11, 22
%t77 = sdiv i32 33, 44
%t78 = add i32 %t76, %t77
%t79 = mul i32 66, 55
%t80 = sub i32 %t78, %t79
%t81 = add i32 %t80, 77
%t82 = mul i32 11, 22
%t83 = add i32 77, %t82
%t84 = sdiv i32 33, 44
%t85 = add i32 %t83, %t84
%t86 = mul i32 55, 66
%t87 = sub i32 %t85, %t86
%t88 = mul i32 11, 22
%t89 = sdiv i32 33, 44
%t90 = add i32 %t88, %t89
%t91 = mul i32 55, 66
%t92 = sub i32 %t90, %t91
%t93 = add i32 %t92, 77
%t94 = sdiv i32 33, 44
%t95 = mul i32 11, 22
%t96 = add i32 %t94, %t95
%t97 = mul i32 55, 66
%t98 = sub i32 %t96, %t97
%t99 = add i32 %t98, 77
%t100 = add i32 11, 22
%t101 = add i32 %t100, 33
%t102 = add i32 %t101, 44
%t103 = add i32 %t102, 55
%t104 = add i32 %t103, 66
%t105 = add i32 %t104, 77
%t106 = add i32 %t105, %t1
%t107 = add i32 %t106, %t2
%t108 = add i32 %t107, %t3
%t109 = add i32 %t108, %t9
%t110 = add i32 %t109, %t15
%t111 = add i32 %t110, %t21
%t112 = add i32 %t111, %t27
%t113 = add i32 %t112, %t33
%t114 = add i32 %t113, %t39
%t115 = add i32 %t114, %t45
%t116 = add i32 %t115, %t51
%t117 = add i32 %t116, %t57
%t118 = add i32 %t117, %t63
%t119 = add i32 %t118, %t69
%t120 = add i32 %t119, %t75
%t121 = add i32 %t120, %t81
%t122 = add i32 %t121, %t87
%t123 = add i32 %t122, %t93
%t124 = add i32 %t123, %t99
ret i32 %t124
}
define i32 @hoisting() {
l1:
br label %l2
l2:
%t1 = phi i32 [5, %l3], [0, %l1]
%t2 = phi i32 [%t2, %l3], [1, %l1]
%t3 = phi i32 [%t3, %l3], [2, %l1]
%t5 = phi i32 [%t5, %l3], [3, %l1]
%t7 = phi i32 [%t6, %l3], [0, %l1]
%t8 = phi i32 [%t8, %l3], [4, %l1]
%t11 = phi i32 [%t10, %l3], [0, %l1]
%t12 = phi i32 [%t13, %l3], [0, %l1]
%t14 = icmp slt i32 %t12, 1000000
br i1 %t14, label %l3, label %l4
l3:
%t4 = add i32 %t2, %t3
%t6 = add i32 %t4, %t5
%t9 = add i32 %t5, %t8
%t10 = add i32 %t9, %t6
%t13 = add i32 %t12, 1
br label %l2
l4:
ret i32 %t3
}
define i32 @doubleIf() {
l1:
br label %l2
l2:
%t3 = icmp eq i32 1, 1
br i1 %t3, label %l3, label %l8
l3:
br label %l4
l4:
%t4 = icmp eq i32 1, 1
br i1 %t4, label %l5, label %l6
l5:
br label %l7
l6:
br label %l7
l7:
%t1 = phi i32 [0, %l5], [0, %l6]
br label %l8
l8:
%t2 = phi i32 [0, %l2], [50, %l7]
ret i32 %t2
}
define i32 @integerDivide() {
l1:
%t1 = sdiv i32 3000, 2
%t2 = mul i32 %t1, 4
%t3 = sdiv i32 %t2, 8
%t4 = sdiv i32 %t3, 16
%t5 = mul i32 %t4, 32
%t6 = sdiv i32 %t5, 64
%t7 = mul i32 %t6, 128
%t8 = sdiv i32 %t7, 4
ret i32 %t8
}
define i32 @association() {
l1:
%t1 = mul i32 10, 2
%t2 = sdiv i32 %t1, 2
%t3 = mul i32 3, %t2
%t4 = sdiv i32 %t3, 3
%t5 = mul i32 %t4, 4
%t6 = sdiv i32 %t5, 4
%t7 = add i32 %t6, 4
%t8 = sub i32 %t7, 4
%t9 = mul i32 %t8, 50
%t10 = sdiv i32 %t9, 50
ret i32 %t10
}
define i32 @tailRecursionHelper(i32 %value, i32 %sum) {
l1:
br label %l2
l2:
%t4 = icmp eq i32 %value, 0
br i1 %t4, label %l3, label %l4
l3:
ret i32 %sum
l4:
%t1 = sub i32 %value, 1
%t2 = add i32 %sum, %value
%t3 = call i32 @tailRecursionHelper(i32 %t1, i32 %t2)
ret i32 %t3
}
define i32 @tailRecursion(i32 %value) {
l1:
%t1 = call i32 @tailRecursionHelper(i32 %value, i32 0)
ret i32 %t1
}
define i32 @unswitching() {
l1:
br label %l2
l2:
%t1 = phi i32 [%t7, %l7], [1, %l1]
%t4 = icmp slt i32 %t1, 1000000
br i1 %t4, label %l3, label %l8
%t5 = phi i32 [%t8, %l7], [2, %l1]
l3:
br label %l4
l4:
%t6 = icmp eq i32 %t5, 2
br i1 %t6, label %l5, label %l6
l5:
%t2 = add i32 %t1, 1
br label %l7
l6:
%t3 = add i32 %t1, 2
br label %l7
l7:
%t8 = phi i32 [%t5, %l5], [%t5, %l6]
%t7 = phi i32 [%t2, %l5], [%t3, %l6]
br label %l2
l8:
ret i32 %t1
}
define i32 @randomCalculation(i32 %number) {
l1:
br label %l2
l2:
%t1 = phi i32 [4, %l3], [0, %l1]
%t2 = phi i32 [7, %l3], [0, %l1]
%t3 = phi i32 [8, %l3], [0, %l1]
%t5 = phi i32 [%t4, %l3], [0, %l1]
%t7 = phi i32 [%t6, %l3], [0, %l1]
%t8 = phi i32 [%t9, %l3], [0, %l1]
%t10 = phi i32 [%t17, %l3], [0, %l1]
%t18 = phi i32 [%t18, %l3], [%number, %l1]
%t19 = icmp slt i32 %t10, %t18
br i1 %t19, label %l3, label %l4
l3:
%t4 = add i32 4, 7
%t6 = add i32 %t4, 8
%t9 = add i32 %t8, %t6
%t11 = mul i32 %t10, 2
%t12 = sdiv i32 %t11, 2
%t13 = mul i32 3, %t12
%t14 = sdiv i32 %t13, 3
%t15 = mul i32 %t14, 4
%t16 = sdiv i32 %t15, 4
%t17 = add i32 %t16, 1
br label %l2
l4:
ret i32 %t8
}
define i32 @iterativeFibonacci(i32 %number) {
l1:
%t1 = mul i32 -1, 1
br label %l2
l2:
%t2 = phi i32 [%t4, %l3], [1, %l1]
%t3 = phi i32 [%t2, %l3], [%t1, %l1]
%t5 = phi i32 [%t4, %l3], [0, %l1]
%t6 = phi i32 [%t7, %l3], [0, %l1]
%t8 = phi i32 [%t8, %l3], [%number, %l1]
%t9 = icmp slt i32 %t6, %t8
br i1 %t9, label %l3, label %l4
l3:
%t4 = add i32 %t2, %t3
%t7 = add i32 %t6, 1
br label %l2
l4:
ret i32 %t2
}
define i32 @recursiveFibonacci(i32 %number) {
l1:
br label %l2
l2:
%t6 = icmp sle i32 %number, 0
%t7 = icmp eq i32 %number, 1
%t8 = or i1 %t6, %t7
br i1 %t8, label %l3, label %l4
l3:
ret i32 %number
l4:
%t1 = sub i32 %number, 1
%t2 = call i32 @recursiveFibonacci(i32 %t1)
%t3 = sub i32 %number, 2
%t4 = call i32 @recursiveFibonacci(i32 %t3)
%t5 = add i32 %t2, %t4
ret i32 %t5
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
br label %l2
l2:
%t5 = phi i32 [%t35, %l3], [0, %l1]
%t23 = phi i32 [%t23, %l3], [%t3, %l1]
%t37 = phi i32 [%t38, %l3], [1, %l1]
%t40 = icmp slt i32 %t37, %t23
br i1 %t40, label %l3, label %l4
l3:
%t4 = call i32 @constantFolding()
%t6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)
%t7 = call i32 @constantPropagation()
%t8 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t7)
%t9 = call i32 @deadCodeElimination()
%t10 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t9)
%t11 = call i32 @interProceduralOptimization()
%t12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t11)
%t13 = call i32 @commonSubexpressionElimination()
%t14 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t13)
%t15 = call i32 @hoisting()
%t16 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t15)
%t17 = call i32 @doubleIf()
%t18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t17)
%t19 = call i32 @integerDivide()
%t20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t19)
%t21 = call i32 @association()
%t22 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t21)
%t24 = sdiv i32 %t23, 1000
%t25 = call i32 @tailRecursion(i32 %t24)
%t26 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t25)
%t27 = call i32 @unswitching()
%t28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t27)
%t29 = call i32 @randomCalculation(i32 %t23)
%t30 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t29)
%t31 = sdiv i32 %t23, 5
%t32 = call i32 @iterativeFibonacci(i32 %t31)
%t33 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t32)
%t34 = sdiv i32 %t23, 1000
%t35 = call i32 @recursiveFibonacci(i32 %t34)
%t36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t35)
%t38 = add i32 %t37, 1
br label %l2
l4:
%t39 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 9999)
ret i32 0
}
attributes #0 = { noinline nounwind optnone ssp uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #1 = { allocsize(0) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #2 = { allocsize(0) }
!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 1}
!3 = !{i32 7, !"frame-pointer", i32 2}
!4 = !{!"Homebrew clang version 13.0.1"}
