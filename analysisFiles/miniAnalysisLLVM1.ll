; ModuleID = 'PLACEHOLDER_NAME.bc'
source_filename = "PLACEHOLDER_NAME.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"
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
%t1 = load i32, i32* %check
%t2 = icmp slt i1 %t1, 100000
l3:
br i1 %t2, label %l4, label %l5
l4:
%t6 = load i32, i32* %check
%t7 = icmp slt i1 %t6, 50000
br i1 %t7, label %l8, label %l9
l8:
%t11 = load i32, i32* %val1
%t12 = add i32 %t11, 1
store i32 %t12, i32* %val1
br label %l10
l9:
%t13 = load i32, i32* %val2
%t14 = add i32 %t13, 1
store i32 %t14, i32* %val2
br label %l10
l10:
%t15 = load i32, i32* %check
%t16 = add i32 %t15, 1
store i32 %t16, i32* %check
br label %l3
l5:
%t17 = load i32, i32* %check
ret i32 %t17
}
attributes #0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
!llvm.module.flags = !{!0}
!llvm.ident = !{!1}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
