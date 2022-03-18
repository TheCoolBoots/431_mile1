target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.simple = type {i32}
%struct.foo = type {i32, i32, %struct.simple*}
@globalfoo = common dso_local global %struct.foo* null
define void @tailrecursive(i32 %num) {
l1:
br label %l2
l2:
%t2 = icmp sle i32 %num, 0
br i1 %t2, label %l3, label %l4
l3:
ret void
l4:
%t1 = sub i32 %num, 1
call void @tailrecursive(i32 %t1)
ret void
}
define i32 @add(i32 %x, i32 %y) {
l1:
%t1 = add i32 %x, %y
ret i32 %t1
}
define void @domath(i32 %num) {
l1:
%t1 = call i8* @malloc(i32 12)
%t2 = bitcast i8* %t1 to %struct.foo*
%t3 = call i8* @malloc(i32 4)
%t4 = bitcast i8* %t3 to %struct.simple*
%t5 = getelementptr %struct.foo, %struct.foo* %t2, i32 0, i32 2
store %struct.simple* %t4, %struct.simple** %t5
%t6 = call i8* @malloc(i32 12)
%t7 = bitcast i8* %t6 to %struct.foo*
%t8 = call i8* @malloc(i32 4)
%t9 = bitcast i8* %t8 to %struct.simple*
%t10 = getelementptr %struct.foo, %struct.foo* %t7, i32 0, i32 2
store %struct.simple* %t9, %struct.simple** %t10
%t11 = getelementptr %struct.foo, %struct.foo* %t2, i32 0, i32 0
store i32 %num, i32* %t11
%t12 = getelementptr %struct.foo, %struct.foo* %t7, i32 0, i32 0
store i32 3, i32* %t12
%t13 = getelementptr %struct.foo, %struct.foo* %t2, i32 0, i32 0
%t14 = load i32, i32* %t13
%t15 = getelementptr %struct.foo, %struct.foo* %t2, i32 0, i32 2
%t16 = getelementptr %struct.simple, %struct.simple* %t15, i32 0, i32 0
store i32 %t14, i32* %t16
%t17 = getelementptr %struct.foo, %struct.foo* %t7, i32 0, i32 0
%t18 = load i32, i32* %t17
%t19 = getelementptr %struct.foo, %struct.foo* %t7, i32 0, i32 2
%t20 = getelementptr %struct.simple, %struct.simple* %t19, i32 0, i32 0
store i32 %t18, i32* %t20
br label %l2
l2:
%t21 = phi %struct.foo* [%t21, %l3], [%t2, %l1]
%t24 = phi %struct.foo* [%t24, %l3], [%t7, %l1]
%t28 = phi i32 [%t46, %l3], [0, %l1]
%t47 = phi i32 [%t48, %l3], [%num, %l1]
%t57 = icmp sgt i32 %t47, 0
br i1 %t57, label %l3, label %l4
l3:
%t22 = getelementptr %struct.foo, %struct.foo* %t21, i32 0, i32 0
%t23 = load i32, i32* %t22
%t25 = getelementptr %struct.foo, %struct.foo* %t24, i32 0, i32 0
%t26 = load i32, i32* %t25
%t27 = mul i32 %t23, %t26
%t29 = getelementptr %struct.foo, %struct.foo* %t21, i32 0, i32 2
%t30 = getelementptr %struct.simple, %struct.simple* %t29, i32 0, i32 0
%t31 = load i32, i32* %t30
%t32 = mul i32 %t27, %t31
%t33 = getelementptr %struct.foo, %struct.foo* %t24, i32 0, i32 0
%t34 = load i32, i32* %t33
%t35 = sdiv i32 %t32, %t34
%t36 = getelementptr %struct.foo, %struct.foo* %t24, i32 0, i32 2
%t37 = getelementptr %struct.simple, %struct.simple* %t36, i32 0, i32 0
%t38 = load i32, i32* %t37
%t39 = getelementptr %struct.foo, %struct.foo* %t21, i32 0, i32 0
%t40 = load i32, i32* %t39
%t41 = call i32 @add(i32 %t38, i32 %t40)
%t42 = getelementptr %struct.foo, %struct.foo* %t24, i32 0, i32 0
%t43 = load i32, i32* %t42
%t44 = getelementptr %struct.foo, %struct.foo* %t21, i32 0, i32 0
%t45 = load i32, i32* %t44
%t46 = sub i32 %t43, %t45
%t48 = sub i32 %t47, 1
br label %l2
l4:
%t49 = getelementptr %struct.foo, %struct.foo* %t21, i32 0, i32 2
%t50 = load %struct.simple*, %struct.simple** %t49
%t51 = bitcast %struct.simple* %t%t50 to i8*
call void @free(i8* %t51)
%t52 = getelementptr %struct.foo, %struct.foo* %t24, i32 0, i32 2
%t53 = load %struct.simple*, %struct.simple** %t52
%t54 = bitcast %struct.simple* %t%t53 to i8*
call void @free(i8* %t54)
%t55 = bitcast %struct.foo* %t%t21 to i8*
call void @free(i8* %t55)
%t56 = bitcast %struct.foo* %t%t24 to i8*
call void @free(i8* %t56)
}
define void @objinstantiation(i32 %num) {
l1:
br label %l2
l2:
%t3 = phi %struct.foo* [%t2, %l3], [0, %l1]
%t5 = phi i32 [%t6, %l3], [%num, %l1]
%t7 = icmp sgt i32 %t5, 0
br i1 %t7, label %l3, label %l4
l3:
%t1 = call i8* @malloc(i32 12)
%t2 = bitcast i8* %t1 to %struct.foo*
%t4 = bitcast %struct.foo* %t%t2 to i8*
call void @free(i8* %t4)
%t6 = sub i32 %t5, 1
br label %l2
l4:
}
define i32 @ackermann(i32 %m, i32 %n) {
l1:
br label %l2
l2:
%t8 = icmp eq i32 %m, 0
br i1 %t8, label %l3, label %l4
l3:
%t1 = add i32 %n, 1
ret i32 %t1
l4:
br label %l5
l5:
%t9 = icmp eq i32 %n, 0
br i1 %t9, label %l6, label %l7
l6:
%t2 = sub i32 %m, 1
%t3 = call i32 @ackermann(i32 %t2, i32 1)
ret i32 %t3
l7:
%t4 = sub i32 %m, 1
%t5 = sub i32 %n, 1
%t6 = call i32 @ackermann(i32 %m, i32 %t5)
%t7 = call i32 @ackermann(i32 %t4, i32 %t6)
ret i32 %t7
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
%t4 = alloca i32
%t5 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t4)
%t6 = load i32, i32* %t4
%t7 = alloca i32
%t8 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t7)
%t9 = load i32, i32* %t7
%t10 = alloca i32
%t11 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t10)
%t12 = load i32, i32* %t10
%t13 = alloca i32
%t14 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t13)
%t15 = load i32, i32* %t13
call void @tailrecursive(i32 %t3)
%t16 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t3)
call void @domath(i32 %t6)
%t17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t6)
call void @objinstantiation(i32 %t9)
%t18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t9)
%t19 = call i32 @ackermann(i32 %t12, i32 %t15)
%t20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t19)
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
