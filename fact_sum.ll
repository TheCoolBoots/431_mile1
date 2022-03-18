target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
define i32 @sum(i32 %a, i32 %b) {
l1:
%t1 = add i32 %a, %b
ret i32 %t1
}
define i32 @fact(i32 %n) {
l1:
br label %l2
l2:
%t7 = icmp eq i32 %n, 1
%t8 = icmp eq i32 %n, 0
%t9 = or i1 %t7, %t8
br i1 %t9, label %l3, label %l4
l3:
ret i32 1
l4:
br label %l5
l5:
%t10 = icmp sle i32 %n, 1
br i1 %t10, label %l6, label %l7
l6:
%t1 = mul i32 -1, 1
%t2 = mul i32 %t1, %n
%t3 = call i32 @fact(i32 %t2)
ret i32 %t3
l7:
%t4 = sub i32 %n, 1
%t5 = call i32 @fact(i32 %t4)
%t6 = mul i32 %n, %t5
ret i32 %t6
}
define i32 @main() {
l1:
br label %l2
l2:
%t4 = phi i32 [%t9, %l3], [0, %l1]
%t8 = phi i32 [%t10, %l3], [0, %l1]
%t16 = phi i32 [%t15, %l3], [0, %l1]
%t17 = mul i32 -1, 1
%t18 = icmp ne i32 %t16, %t17
br i1 %t18, label %l3, label %l4
l3:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
%t5 = alloca i32
%t6 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t5)
%t7 = load i32, i32* %t5
%t9 = call i32 @fact(i32 %t3)
%t10 = call i32 @fact(i32 %t7)
%t11 = call i32 @sum(i32 %t9, i32 %t10)
%t12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t11)
%t13 = alloca i32
%t14 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t13)
%t15 = load i32, i32* %t13
br label %l2
l4:
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
