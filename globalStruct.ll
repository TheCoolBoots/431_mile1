target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.A = type {i32, i32}
@a = common dso_local global %struct.A* null
@b = common dso_local global %struct.A* null
define i32 @main() {
l1:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.A*
store %struct.A* %t2, %struct.A** @a
%t3 = call i8* @malloc(i32 8)
%t4 = bitcast i8* %t3 to %struct.A*
store %struct.A* %t4, %struct.A** @b
%t5 = getelementptr %struct.A, %struct.A** @a, i32 0, i32 0
store i32 1, i32* %t5
%t6 = getelementptr %struct.A, %struct.A** @b, i32 0, i32 1
store i32 2, i32* %t6
%t7 = load %struct.A** @b
store %struct.A* %t7, %struct.A** @a
%t8 = getelementptr %struct.A, %struct.A* @a, i32 0, i32 1
%t9 = load i32, i32* %t8
ret i32 %t9
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
