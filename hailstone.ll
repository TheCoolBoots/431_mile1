target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
define i32 @mod(i32 %a, i32 %b) {
l1:
%t1 = sdiv i32 %a, %b
%t2 = mul i32 %t1, %b
%t3 = sub i32 %a, %t2
ret i32 %t3
}
define void @hailstone(i32 %n) {
l1:
br label %l2
l2:
%t1 = phi i32 [%t6, %l10], [%n, %l1]
br i1 1, label %l3, label %l11
l3:
%t2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t1)
br label %l4
l4:
%t8 = call i32 @mod(i32 %t1, i32 2)
%t9 = icmp eq i32 %t8, 1
br i1 %t9, label %l5, label %l6
l5:
%t3 = mul i32 3, %t1
%t4 = add i32 %t3, 1
br label %l7
l6:
%t5 = sdiv i32 %t1, 2
br label %l7
l7:
%t6 = phi i32 [%t4, %l5], [%t5, %l6]
br label %l8
l8:
%t10 = icmp sle i32 %t6, 1
br i1 %t10, label %l9, label %l10
l9:
%t7 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t6)
ret void
l10:
br label %l2
l11:
ret void
}
define i32 @main() {
l1:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
call void @hailstone(i32 %t3)
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
