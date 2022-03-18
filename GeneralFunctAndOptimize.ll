ERROR: unrecognized structure in AST 
[<ast_class_definitions.m_id object at 0x10ca76230>]
ERROR: unrecognized structure in AST 
[<ast_class_definitions.m_id object at 0x10cb7d5d0>]
ERROR: unrecognized structure in AST 
[<ast_class_definitions.m_id object at 0x10cb7d630>]
ERROR: unrecognized m_statement:[<ast_class_definitions.m_id object at 0x10ca76230>]
ERROR: unrecognized m_statement:[<ast_class_definitions.m_id object at 0x10cb7d5d0>]
ERROR: unrecognized m_statement:[<ast_class_definitions.m_id object at 0x10cb7d630>]
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.IntHolder = type {i32}
@interval = common dso_local global i32 0
@end = common dso_local global i32 0
define i32 @multBy4xTimes(%struct.IntHolder* %num, i32 %timesLeft) {
l1:
br label %l2
l2:
%t9 = icmp sle i32 %timesLeft, 0
br i1 %t9, label %l3, label %l4
l3:
%t1 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t2 = load i32, i32* %t1
ret i32 %t2
l4:
%t3 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t4 = load i32, i32* %t3
%t5 = mul i32 4, %t4
%t6 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
store i32 %t5, i32* %t6
%t7 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t8 = load i32, i32* %t7
ret i32 %t8
}
define void @divideBy8(%struct.IntHolder* %num) {
l1:
%t1 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t2 = load i32, i32* %t1
%t3 = div i32 %t2, 2
%t4 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
store i32 %t3, i32* %t4
%t5 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t6 = load i32, i32* %t5
%t7 = div i32 %t6, 2
%t8 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
store i32 %t7, i32* %t8
%t9 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
%t10 = load i32, i32* %t9
%t11 = div i32 %t10, 2
%t12 = getelementptr %struct.IntHolder, %struct.IntHolder* %num, i32 0, i32 0
store i32 %t11, i32* %t12
}
define i32 @main() {
l1:
%t1 = call i8* @malloc(i32 4)
%t2 = bitcast i8* %t1 to %struct.IntHolder*
store i32 1000000, i32* @end
%t3 = alloca i32
%t4 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t3)
%t5 = load i32, i32* %t3
%t6 = alloca i32
%t7 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t6)
%t8 = load i32, i32* %t6
store i32 %t8, i32* @interval
%t9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t5)
%t10 = load i32* @interval
%t11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t10)
br label %l2
l2:
%t56 = phi i1 [%t35, %l9], [null, %l1]
%t54 = phi i32 [%t33, %l9], [null, %l1]
%t53 = phi i32 [%t30, %l9], [null, %l1]
%t51 = phi %struct.IntHolder* [%t26, %l9], [%t2, %l1]
%t12 = phi i32 [%t24, %l9], [0, %l1]
%t42 = phi i32 [%t23, %l9], [0, %l1]
%t44 = phi i32 [%t40, %l9], [0, %l1]
%t45 = icmp slt i32 %t44, 50
br i1 %t45, label %l3, label %l10
l3:
br label %l4
l4:
%t23 = phi i32 [%t49, %l8], [%t42, %l3]
%t24 = phi i32 [%t38, %l8], [0, %l3]
%t26 = phi %struct.IntHolder* [%t50, %l8], [%t51, %l3]
%t30 = phi i32 [%t52, %l8], [%t53, %l3]
%t33 = phi i32 [%t37, %l8], [%t54, %l3]
%t35 = phi i1 [%t55, %l8], [%t56, %l3]
%t39 = phi i32 [%t57, %l8], [%t44, %l3]
%t46 = load i32* @end
%t47 = icmp sle i32 %t24, %t46
br i1 %t47, label %l5, label %l9
l5:
%t13 = mul i32 1, 2
%t14 = mul i32 %t13, 3
%t15 = mul i32 %t14, 4
%t16 = mul i32 %t15, 5
%t17 = mul i32 %t16, 6
%t18 = mul i32 %t17, 7
%t19 = mul i32 %t18, 8
%t20 = mul i32 %t19, 9
%t21 = mul i32 %t20, 10
%t22 = mul i32 %t21, 11
%t25 = add i32 %t24, 1
%t27 = getelementptr %struct.IntHolder, %struct.IntHolder* %t26, i32 0, i32 0
store i32 %t25, i32* %t27
%t28 = getelementptr %struct.IntHolder, %struct.IntHolder* %t26, i32 0, i32 0
%t29 = load i32, i32* %t28
%t31 = load i32* @interval
%t32 = sub i32 %t31, 1
%t34 = icmp sle i32 %t32, 0
br label %l6
l6:
%t48 = icmp sle i32 %t32, 0
br i1 %t48, label %l7, label %l8
l7:
br label %l8
l8:
%t57 = phi i32 [%t39, %l6], [%t39, %l7]
%t55 = phi i1 [%t34, %l6], [%t34, %l7]
%t52 = phi i32 [%t29, %l6], [%t29, %l7]
%t50 = phi %struct.IntHolder* [%t26, %l6], [%t26, %l7]
%t49 = phi i32 [%t22, %l6], [%t22, %l7]
%t37 = phi i32 [%t32, %l6], [1, %l7]
%t36 = phi i32 [%t25, %l6], [%t25, %l7]
%t38 = add i32 %t36, %t37
br label %l4
l9:
%t40 = add i32 %t39, 1
br label %l2
l10:
%t41 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t12)
%t43 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t42)
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
