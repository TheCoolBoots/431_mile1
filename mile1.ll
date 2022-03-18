target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.Power = type {i32, i32}
define i32 @calcPower(i32 %base, i32 %exp) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t3, %l3], [1, %l1]
%t2 = phi i32 [%t2, %l3], [%base, %l1]
%t4 = phi i32 [%t5, %l3], [%exp, %l1]
%t6 = icmp sgt i32 %t4, 0
br i1 %t6, label %l3, label %l4
l3:
%t3 = mul i32 %t1, %t2
%t5 = sub i32 %t4, 1
br label %l2
l4:
ret i32 %t1
}
define i32 @main() {
l1:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.Power*
%t3 = alloca i32
%t4 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t3)
%t5 = load i32, i32* %t3
%t6 = getelementptr %struct.Power, %struct.Power* %t2, i32 0, i32 0
store i32 %t5, i32* %t6
%t7 = alloca i32
%t8 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t7)
%t9 = load i32, i32* %t7
br label %l2
l2:
%t22 = icmp slt i32 %t9, 0
br i1 %t22, label %l3, label %l4
l3:
%t10 = mul i32 -1, 1
ret i32 %t10
l4:
%t11 = getelementptr %struct.Power, %struct.Power* %t2, i32 0, i32 1
store i32 %t9, i32* %t11
br label %l5
l5:
%t12 = phi i32 [%t13, %l6], [0, %l4]
%t14 = phi %struct.Power* [%t14, %l6], [%t2, %l4]
%t20 = phi i32 [%t19, %l6], [0, %l4]
%t23 = icmp slt i32 %t12, 1000000
br i1 %t23, label %l6, label %l7
l6:
%t13 = add i32 %t12, 1
%t15 = getelementptr %struct.Power, %struct.Power* %t14, i32 0, i32 0
%t16 = load i32, i32* %t15
%t17 = getelementptr %struct.Power, %struct.Power* %t14, i32 0, i32 1
%t18 = load i32, i32* %t17
%t19 = call i32 @calcPower(i32 %t16, i32 %t18)
br label %l5
l7:
%t21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t20)
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
