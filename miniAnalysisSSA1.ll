; ModuleID = 'PLACEHOLDER_NAME.bc'
source_filename = "PLACEHOLDER_NAME.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"
declare i8* @malloc(i32)
declare void @free(i8*)
declare i32 @printf(i8*, i32)
declare i32 @scanf(i8*, i32*)
define i32 @main() {
l0:
br label %l1
l1:
%t1 = phi i32 [%t5, %l2], [0, %l0]
%t2 = icmp slt i32 %t1, 50
br i1 %t2, label %l2, label %l3
l2:
%t3 = phi i32 [%t4, %l2], [0, %l0]
%t4 = add i32 %t3, 1
%t5 = add i32 %t1, 2
br label %l1
l3:
%t6 = phi i32 [%t4, %l2], [0, %l0]
%t0 = add i32 %t6, 0
br label %retLabel
retLabel:
ret i32 %t0
}
attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
!llvm.module.flags = !{!0}
!llvm.ident = !{!1}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
