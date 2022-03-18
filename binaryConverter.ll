ERROR: unrecognized structure in AST 
[<ast_class_definitions.m_id object at 0x1066911e0>]
ERROR: unrecognized m_statement:[<ast_class_definitions.m_id object at 0x1066911e0>]
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
define i32 @wait(i32 %waitTime) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t2, %l3], [%waitTime, %l1]
%t3 = icmp sgt i32 %t1, 0
br i1 %t3, label %l3, label %l4
l3:
%t2 = sub i32 %t1, 1
br label %l2
l4:
ret i32 0
}
define i32 @power(i32 %base, i32 %exponent) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t3, %l3], [1, %l1]
%t2 = phi i32 [%t2, %l3], [%base, %l1]
%t4 = phi i32 [%t5, %l3], [%exponent, %l1]
%t6 = icmp sgt i32 %t4, 0
br i1 %t6, label %l3, label %l4
l3:
%t3 = mul i32 %t1, %t2
%t5 = sub i32 %t4, 1
br label %l2
l4:
ret i32 %t1
}
define i32 @recursiveDecimalSum(i32 %binaryNum, i32 %decimalSum, i32 %recursiveDepth) {
l1:
br label %l2
l2:
%t12 = icmp sgt i32 %binaryNum, 0
br i1 %t12, label %l3, label %l7
l3:
%t1 = div i32 %binaryNum, 10
%t2 = mul i32 %t1, 10
%t3 = sub i32 %binaryNum, %t2
br label %l4
l4:
%t13 = icmp eq i32 %t3, 1
br i1 %t13, label %l5, label %l6
l5:
%t4 = call i32 @power(i32 2, i32 %recursiveDepth)
%t5 = add i32 %decimalSum, %t4
br label %l6
l6:
%t9 = phi i32 [%recursiveDepth, %l4], [%recursiveDepth, %l5]
%t8 = phi i32 [%decimalSum, %l4], [%t5, %l5]
%t6 = phi i32 [%binaryNum, %l4], [%binaryNum, %l5]
%t7 = div i32 %t6, 10
%t10 = add i32 %t9, 1
%t11 = call i32 @recursiveDecimalSum(i32 %t7, i32 %t8, i32 %t10)
ret i32 %t11
l7:
ret i32 %decimalSum
}
define i32 @convertToDecimal(i32 %binaryNum) {
l1:
%t1 = call i32 @recursiveDecimalSum(i32 %binaryNum, i32 0, i32 0)
ret i32 %t1
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
%t4 = call i32 @convertToDecimal(i32 %t3)
%t5 = mul i32 %t4, %t4
br label %l2
l2:
%t6 = phi i32 [%t7, %l3], [%t5, %l1]
%t8 = phi i32 [%t8, %l3], [%t4, %l1]
%t10 = icmp sgt i32 %t6, 0
br i1 %t10, label %l3, label %l4
l3:
%t7 = sub i32 %t6, 1
br label %l2
l4:
%t9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t8)
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
