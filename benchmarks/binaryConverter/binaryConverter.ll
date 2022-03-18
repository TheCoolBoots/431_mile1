; ModuleID = 'binaryConverter.bc'
source_filename = "binaryConverter.c"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"

@.str = private unnamed_addr constant [4 x i8] c"%ld\00", align 1
@.str.1 = private unnamed_addr constant [5 x i8] c"%ld\0A\00", align 1

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_wait(i64 %0) #0 {
  %2 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  br label %3

3:                                                ; preds = %6, %1
  %4 = load i64, i64* %2, align 8
  %5 = icmp sgt i64 %4, 0
  br i1 %5, label %6, label %9

6:                                                ; preds = %3
  %7 = load i64, i64* %2, align 8
  %8 = sub nsw i64 %7, 1
  store i64 %8, i64* %2, align 8
  br label %3, !llvm.loop !5

9:                                                ; preds = %3
  ret i64 0
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_power(i64 %0, i64 %1) #0 {
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  store i64 %0, i64* %3, align 8
  store i64 %1, i64* %4, align 8
  store i64 1, i64* %5, align 8
  br label %6

6:                                                ; preds = %9, %2
  %7 = load i64, i64* %4, align 8
  %8 = icmp sgt i64 %7, 0
  br i1 %8, label %9, label %15

9:                                                ; preds = %6
  %10 = load i64, i64* %5, align 8
  %11 = load i64, i64* %3, align 8
  %12 = mul nsw i64 %10, %11
  store i64 %12, i64* %5, align 8
  %13 = load i64, i64* %4, align 8
  %14 = sub nsw i64 %13, 1
  store i64 %14, i64* %4, align 8
  br label %6, !llvm.loop !7

15:                                               ; preds = %6
  %16 = load i64, i64* %5, align 8
  ret i64 %16
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_recursiveDecimalSum(i64 %0, i64 %1, i64 %2) #0 {
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca i64, align 8
  %8 = alloca i64, align 8
  %9 = alloca i64, align 8
  %10 = alloca i64, align 8
  store i64 %0, i64* %5, align 8
  store i64 %1, i64* %6, align 8
  store i64 %2, i64* %7, align 8
  %11 = load i64, i64* %5, align 8
  %12 = icmp sgt i64 %11, 0
  br i1 %12, label %13, label %36

13:                                               ; preds = %3
  store i64 2, i64* %9, align 8
  %14 = load i64, i64* %5, align 8
  %15 = sdiv i64 %14, 10
  store i64 %15, i64* %8, align 8
  %16 = load i64, i64* %8, align 8
  %17 = mul nsw i64 %16, 10
  store i64 %17, i64* %8, align 8
  %18 = load i64, i64* %5, align 8
  %19 = load i64, i64* %8, align 8
  %20 = sub nsw i64 %18, %19
  store i64 %20, i64* %8, align 8
  %21 = load i64, i64* %8, align 8
  %22 = icmp eq i64 %21, 1
  br i1 %22, label %23, label %29

23:                                               ; preds = %13
  %24 = load i64, i64* %6, align 8
  %25 = load i64, i64* %9, align 8
  %26 = load i64, i64* %7, align 8
  %27 = call i64 @_mini_power(i64 %25, i64 %26)
  %28 = add nsw i64 %24, %27
  store i64 %28, i64* %6, align 8
  br label %29

29:                                               ; preds = %23, %13
  %30 = load i64, i64* %5, align 8
  %31 = sdiv i64 %30, 10
  %32 = load i64, i64* %6, align 8
  %33 = load i64, i64* %7, align 8
  %34 = add nsw i64 %33, 1
  %35 = call i64 @_mini_recursiveDecimalSum(i64 %31, i64 %32, i64 %34)
  store i64 %35, i64* %4, align 8
  br label %38

36:                                               ; preds = %3
  %37 = load i64, i64* %6, align 8
  store i64 %37, i64* %4, align 8
  br label %38

38:                                               ; preds = %36, %29
  %39 = load i64, i64* %4, align 8
  ret i64 %39
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_convertToDecimal(i64 %0) #0 {
  %2 = alloca i64, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  store i64 0, i64* %3, align 8
  store i64 0, i64* %4, align 8
  %5 = load i64, i64* %2, align 8
  %6 = load i64, i64* %4, align 8
  %7 = load i64, i64* %3, align 8
  %8 = call i64 @_mini_recursiveDecimalSum(i64 %5, i64 %6, i64 %7)
  ret i64 %8
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_main() #0 {
  %1 = alloca i64, align 8
  %2 = alloca i64, align 8
  %3 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i64* %1)
  %4 = load i64, i64* %1, align 8
  %5 = call i64 @_mini_convertToDecimal(i64 %4)
  store i64 %5, i64* %1, align 8
  %6 = load i64, i64* %1, align 8
  %7 = load i64, i64* %1, align 8
  %8 = mul nsw i64 %6, %7
  store i64 %8, i64* %2, align 8
  br label %9

9:                                                ; preds = %12, %0
  %10 = load i64, i64* %2, align 8
  %11 = icmp sgt i64 %10, 0
  br i1 %11, label %12, label %17

12:                                               ; preds = %9
  %13 = load i64, i64* %2, align 8
  %14 = call i64 @_mini_wait(i64 %13)
  %15 = load i64, i64* %2, align 8
  %16 = sub nsw i64 %15, 1
  store i64 %16, i64* %2, align 8
  br label %9, !llvm.loop !8

17:                                               ; preds = %9
  %18 = load i64, i64* %1, align 8
  %19 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i64 %18)
  ret i64 0
}

declare i32 @scanf(i8*, ...) #1

declare i32 @printf(i8*, ...) #1

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i64 @_mini_main()
  %3 = trunc i64 %2 to i32
  ret i32 %3
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
!7 = distinct !{!7, !6}
!8 = distinct !{!8, !6}
