target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.linkedNums = type {i32, %struct.linkedNums*}
define %struct.linkedNums* @getRands(i32 %seed, i32 %num) {
l1:
%t1 = mul i32 %seed, %seed
%t2 = call i8* @malloc(i32 8)
%t3 = bitcast i8* %t2 to %struct.linkedNums*
%t4 = getelementptr %struct.linkedNums, %struct.linkedNums* %t3, i32 0, i32 0
store i32 %t1, i32* %t4
%t5 = getelementptr %struct.linkedNums, %struct.linkedNums* %t3, i32 0, i32 1
store %struct.linkedNums* null, %struct.linkedNums** %t5
%t6 = sub i32 %num, 1
br label %l2
l2:
%t7 = phi i32 [%t17, %l3], [%t1, %l1]
%t9 = phi i32 [%t9, %l3], [%seed, %l1]
%t14 = phi i32 [%t17, %l3], [%t1, %l1]
%t20 = phi %struct.linkedNums* [%t19, %l3], [null, %l1]
%t22 = phi %struct.linkedNums* [%t19, %l3], [%t3, %l1]
%t24 = phi i32 [%t25, %l3], [%t6, %l1]
%t26 = icmp sgt i32 %t24, 0
br i1 %t26, label %l3, label %l4
l3:
%t8 = mul i32 %t7, %t7
%t10 = sdiv i32 %t8, %t9
%t11 = sdiv i32 %t9, 2
%t12 = mul i32 %t10, %t11
%t13 = add i32 %t12, 1
%t15 = sdiv i32 %t13, 1000000000
%t16 = mul i32 %t15, 1000000000
%t17 = sub i32 %t13, %t16
%t18 = call i8* @malloc(i32 8)
%t19 = bitcast i8* %t18 to %struct.linkedNums*
%t21 = getelementptr %struct.linkedNums, %struct.linkedNums* %t19, i32 0, i32 0
store i32 %t17, i32* %t21
%t23 = getelementptr %struct.linkedNums, %struct.linkedNums* %t19, i32 0, i32 1
store %struct.linkedNums* %t22, %struct.linkedNums** %t23
%t25 = sub i32 %t24, 1
br label %l2
l4:
ret %struct.linkedNums* null
}
define i32 @calcMean(%struct.linkedNums* %nums) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t2, %l3], [0, %l1]
%t3 = phi i32 [%t7, %l3], [0, %l1]
%t4 = phi %struct.linkedNums* [%t9, %l3], [%nums, %l1]
%t11 = phi i32 [%t11, %l3], [0, %l1]
%t13 = icmp ne %struct.linkedNums* %t4, null
br i1 %t13, label %l3, label %l4
l3:
%t2 = add i32 %t1, 1
%t5 = getelementptr %struct.linkedNums, %struct.linkedNums* %t4, i32 0, i32 0
%t6 = load i32, i32* %t5
%t7 = add i32 %t3, %t6
%t8 = getelementptr %struct.linkedNums, %struct.linkedNums* %t4, i32 0, i32 1
%t9 = load %struct.linkedNums*, %struct.linkedNums** %t8
br label %l2
l4:
br label %l5
l5:
%t14 = icmp ne i32 %t1, 0
br i1 %t14, label %l6, label %l7
l6:
%t10 = sdiv i32 %t3, %t1
br label %l7
l7:
%t12 = phi i32 [%t11, %l5], [%t10, %l6]
ret i32 %t12
}
define i32 @approxSqrt(i32 %num) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t5, %l3], [1, %l1]
%t3 = phi i32 [%t2, %l3], [0, %l1]
%t4 = phi i32 [%t1, %l3], [1, %l1]
%t6 = phi i32 [%t6, %l3], [%num, %l1]
%t7 = icmp slt i32 %t3, %t6
br i1 %t7, label %l3, label %l4
l3:
%t2 = mul i32 %t1, %t1
%t5 = add i32 %t1, 1
br label %l2
l4:
ret i32 %t4
}
define void @approxSqrtAll(%struct.linkedNums* %nums) {
l1:
br label %l2
l2:
%t1 = phi %struct.linkedNums* [%t7, %l3], [%nums, %l1]
%t8 = icmp ne %struct.linkedNums* %t1, null
br i1 %t8, label %l3, label %l4
l3:
%t2 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t3 = load i32, i32* %t2
%t4 = call i32 @approxSqrt(i32 %t3)
%t5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)
%t6 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 1
%t7 = load %struct.linkedNums*, %struct.linkedNums** %t6
br label %l2
l4:
ret void
}
define void @range(%struct.linkedNums* %nums) {
l1:
br label %l2
l2:
%t1 = phi %struct.linkedNums* [%t17, %l14], [%nums, %l1]
%t4 = phi i32 [%t29, %l14], [0, %l1]
%t7 = phi i32 [%t32, %l14], [0, %l1]
%t8 = phi i1 [%t35, %l14], [1, %l1]
%t20 = icmp ne %struct.linkedNums* %t1, null
br i1 %t20, label %l3, label %l15
l3:
br label %l4
l4:
br i1 %t8, label %l5, label %l6
l5:
%t2 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t3 = load i32, i32* %t2
%t5 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t6 = load i32, i32* %t5
br label %l14
l6:
br label %l7
l7:
%t21 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t22 = load i32, i32* %t21
%t23 = icmp slt i32 %t22, %t4
br i1 %t23, label %l8, label %l9
l8:
%t9 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t10 = load i32, i32* %t9
br label %l13
l9:
br label %l10
l10:
%t24 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t25 = load i32, i32* %t24
%t26 = icmp sgt i32 %t25, %t7
br i1 %t26, label %l11, label %l12
l11:
%t11 = getelementptr %struct.linkedNums, %struct.linkedNums* %t1, i32 0, i32 0
%t12 = load i32, i32* %t11
br label %l12
l12:
%t33 = phi i1 [%t8, %l10], [%t8, %l11]
%t30 = phi i32 [%t7, %l10], [%t12, %l11]
%t27 = phi i32 [%t4, %l10], [%t4, %l11]
%t13 = phi %struct.linkedNums* [%t1, %l10], [%t1, %l11]
br label %l13
l13:
%t34 = phi i1 [%t8, %l8], [%t33, %l12]
%t31 = phi i32 [%t7, %l8], [%t30, %l12]
%t28 = phi i32 [%t10, %l8], [%t27, %l12]
%t14 = phi %struct.linkedNums* [%t1, %l8], [%t13, %l12]
br label %l14
l14:
%t35 = phi i1 [0, %l5], [%t34, %l13]
%t32 = phi i32 [%t6, %l5], [%t31, %l13]
%t29 = phi i32 [%t3, %l5], [%t28, %l13]
%t15 = phi %struct.linkedNums* [%t1, %l5], [%t14, %l13]
%t16 = getelementptr %struct.linkedNums, %struct.linkedNums* %t15, i32 0, i32 1
%t17 = load %struct.linkedNums*, %struct.linkedNums** %t16
br label %l2
l15:
%t18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)
%t19 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t7)
ret void
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
%t4 = alloca i32
%t5 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t4)
%t6 = load i32, i32* %t4
%t7 = call %struct.linkedNums* @getRands(i32 %t3, i32 %t6)
%t8 = call i32 @calcMean(%struct.linkedNums* %t7)
%t9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t8)
call void @range(%struct.linkedNums* %t7)
call void @approxSqrtAll(%struct.linkedNums* %t7)
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
