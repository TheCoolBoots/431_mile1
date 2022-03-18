target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.IntList = type {i32, %struct.IntList*}
define %struct.IntList* @getIntList() {
l1:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.IntList*
%t3 = alloca i32
%t4 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t3)
%t5 = load i32, i32* %t3
br label %l2
l2:
%t11 = mul i32 -1, 1
%t12 = icmp eq i32 %t5, %t11
br i1 %t12, label %l3, label %l4
l3:
%t6 = getelementptr %struct.IntList, %struct.IntList* %t2, i32 0, i32 0
store i32 %t5, i32* %t6
%t7 = getelementptr %struct.IntList, %struct.IntList* %t2, i32 0, i32 1
store %struct.IntList* null, %struct.IntList** %t7
ret %struct.IntList* %t2
l4:
%t8 = getelementptr %struct.IntList, %struct.IntList* %t2, i32 0, i32 0
store i32 %t5, i32* %t8
%t9 = call %struct.IntList* @getIntList()
%t10 = getelementptr %struct.IntList, %struct.IntList* %t2, i32 0, i32 1
store %struct.IntList* %t9, %struct.IntList** %t10
ret %struct.IntList* %t2
}
define i32 @biggest(i32 %num1, i32 %num2) {
l1:
br label %l2
l2:
%t1 = icmp sgt i32 %num1, %num2
br i1 %t1, label %l3, label %l4
l3:
ret i32 %num1
l4:
ret i32 %num2
}
define i32 @biggestInList(%struct.IntList* %list) {
l1:
%t1 = getelementptr %struct.IntList, %struct.IntList* %list, i32 0, i32 0
%t2 = load i32, i32* %t1
br label %l2
l2:
%t3 = phi i32 [%t7, %l3], [%t2, %l1]
%t4 = phi %struct.IntList* [%t9, %l3], [%list, %l1]
%t10 = getelementptr %struct.IntList, %struct.IntList* %t4, i32 0, i32 1
%t11 = load %struct.IntList*, %struct.IntList** %t10
%t12 = icmp ne %struct.IntList* %t11, null
br i1 %t12, label %l3, label %l4
l3:
%t5 = getelementptr %struct.IntList, %struct.IntList* %t4, i32 0, i32 0
%t6 = load i32, i32* %t5
%t7 = call i32 @biggest(i32 %t3, i32 %t6)
%t8 = getelementptr %struct.IntList, %struct.IntList* %t4, i32 0, i32 1
%t9 = load %struct.IntList*, %struct.IntList** %t8
br label %l2
l4:
ret i32 %t3
}
define i32 @main() {
l1:
%t1 = call %struct.IntList* @getIntList()
%t2 = call i32 @biggestInList(%struct.IntList* %t1)
%t3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t2)
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
