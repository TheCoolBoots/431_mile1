target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
define i32 @isqrt(i32 %a) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t3, %l3], [1, %l1]
%t2 = phi i32 [%t4, %l3], [3, %l1]
%t7 = phi i32 [%t7, %l3], [%a, %l1]
%t8 = icmp sle i32 %t1, %t7
br i1 %t8, label %l3, label %l4
l3:
%t3 = add i32 %t1, %t2
%t4 = add i32 %t2, 2
br label %l2
l4:
%t5 = sdiv i32 %t2, 2
%t6 = sub i32 %t5, 1
ret i32 %t6
}
define i1 @prime(i32 %a) {
l1:
br label %l2
l2:
%t9 = icmp slt i32 %a, 2
br i1 %t9, label %l3, label %l4
l3:
ret i1 0
l4:
%t1 = call i32 @isqrt(i32 %a)
br label %l5
l5:
%t2 = phi i32 [%t2, %l9], [%a, %l4]
%t3 = phi i32 [%t8, %l9], [2, %l4]
%t7 = phi i32 [%t6, %l9], [0, %l4]
%t10 = phi i32 [%t10, %l9], [%t1, %l4]
%t11 = icmp sle i32 %t3, %t10
br i1 %t11, label %l6, label %l10
l6:
%t4 = sdiv i32 %t2, %t3
%t5 = mul i32 %t4, %t3
%t6 = sub i32 %t2, %t5
br label %l7
l7:
%t12 = icmp eq i32 %t6, 0
br i1 %t12, label %l8, label %l9
l8:
ret i1 0
l9:
%t8 = add i32 %t3, 1
br label %l5
l10:
ret i1 1
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
br label %l2
l2:
%t4 = phi i32 [%t7, %l6], [0, %l1]
%t8 = phi i32 [%t11, %l6], [%t3, %l1]
%t9 = icmp sle i32 %t4, %t8
br i1 %t9, label %l3, label %l7
l3:
br label %l4
l4:
%t10 = call i1 @prime(i32 %t4)
br i1 %t10, label %l5, label %l6
l5:
%t5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)
br label %l6
l6:
%t11 = phi i32 [%t8, %l4], [%t8, %l5]
%t6 = phi i32 [%t4, %l4], [%t4, %l5]
%t7 = add i32 %t6, 1
br label %l2
l7:
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
