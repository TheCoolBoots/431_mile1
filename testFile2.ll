; ModuleID = 'cAnalysis1.bc'
source_filename = "analysis1.c"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare i8* @malloc(i32)
declare void @free(i8*)
declare i32 @printf(i8*, i32)
declare i32 @scanf(i8*, i32*)
define i32 @main() {
entry:
%check = alloca i32
%val1 = alloca i32
%val2 = alloca i32
store i32 0, i32* %check
store i32 0, i32* %val1
store i32 0, i32* %val2
l3:
%t1 = load i32, i32* %val1
%t2 = icmp slt i1 %t1, 50
br i1 %t2, label %l4, label %l5
l4:
%t6 = load i32, i32* %check
%t7 = add i32 %t6, 1
store i32 %t7, i32* %check
%t8 = load i32, i32* %val1
%t9 = add i32 %t8, 2
store i32 %t9, i32* %val1
br label %l3
l5:
%t10 = load i32, i32* %check
ret i32 %t10
}
attributes #0 = { noinline nounwind optnone ssp uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 7, !"PIC Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 1}
!3 = !{i32 7, !"frame-pointer", i32 2}
!4 = !{!"Homebrew clang version 13.0.1"}
!5 = distinct !{!5, !6}
!6 = !{!"llvm.loop.mustprogress"}
