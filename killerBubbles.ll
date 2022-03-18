target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.Node = type {i32, %struct.Node*, %struct.Node*}
@swapped = common dso_local global i32 0
define i32 @compare(%struct.Node* %a, %struct.Node* %b) {
l1:
%t1 = getelementptr %struct.Node, %struct.Node* %a, i32 0, i32 0
%t2 = load i32, i32* %t1
%t3 = getelementptr %struct.Node, %struct.Node* %b, i32 0, i32 0
%t4 = load i32, i32* %t3
%t5 = sub i32 %t2, %t4
ret i32 %t5
}
define void @deathSort(%struct.Node* %head) {
l1:
br label %l2
l2:
%t29 = phi i32 [%t7, %l9], [0, %l1]
%t1 = phi i32 [%t14, %l9], [1, %l1]
%t2 = phi %struct.Node* [%t22, %l9], [%head, %l1]
%t3 = phi %struct.Node* [%t4, %l9], [null, %l1]
%t18 = load i32, i32* @swapped
%t19 = icmp eq i32 %t18, 1
br i1 %t19, label %l3, label %l10
l3:
br label %l4
l4:
%t4 = phi %struct.Node* [%t17, %l8], [%t2, %l3]
%t7 = phi i32 [%t28, %l8], [%t29, %l3]
%t14 = phi i32 [%t30, %l8], [0, %l3]
%t20 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 2
%t21 = load %struct.Node*, %struct.Node** %t20
%t22 = phi %struct.Node* [%t31, %l8], [%t2, %l3]
%t23 = icmp ne %struct.Node* %t21, %t22
br i1 %t23, label %l5, label %l9
l5:
br label %l6
l6:
%t24 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 2
%t25 = load %struct.Node*, %struct.Node** %t24
%t26 = call i32 @compare(%struct.Node* %t4, %struct.Node* %t25)
%t27 = icmp sgt i32 %t26, 0
br i1 %t27, label %l7, label %l8
l7:
%t5 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 0
%t6 = load i32, i32* %t5
%t8 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 2
%t9 = getelementptr %struct.Node, %struct.Node* %t8, i32 0, i32 0
%t10 = load i32, i32* %t9
%t11 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 0
store i32 %t10, i32* %t11
%t12 = getelementptr %struct.Node, %struct.Node* %t4, i32 0, i32 2
%t13 = getelementptr %struct.Node, %struct.Node* %t12, i32 0, i32 0
store i32 %t6, i32* %t13
br label %l8
l8:
%t31 = phi %struct.Node* [%t22, %l6], [%t22, %l7]
%t30 = phi i32 [%t14, %l6], [1, %l7]
%t28 = phi i32 [%t7, %l6], [%t6, %l7]
%t15 = phi %struct.Node* [%t4, %l6], [%t4, %l7]
%t16 = getelementptr %struct.Node, %struct.Node* %t15, i32 0, i32 2
%t17 = load %struct.Node*, %struct.Node** %t16
br label %l4
l9:
br label %l2
l10:
}
define i32 @main() {
l1:
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
