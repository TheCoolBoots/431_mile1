; ModuleID = 'stats.bc'
source_filename = "stats.c"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"

%struct._mini_linkedNums = type { i64, %struct._mini_linkedNums* }

@.str = private unnamed_addr constant [5 x i8] c"%ld\0A\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%ld\00", align 1

; Function Attrs: noinline nounwind optnone ssp uwtable
define %struct._mini_linkedNums* @_mini_getRands(i64 %0, i64 %1) #0 {
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  %6 = alloca i64, align 8
  %7 = alloca %struct._mini_linkedNums*, align 8
  %8 = alloca %struct._mini_linkedNums*, align 8
  store i64 %0, i64* %3, align 8
  store i64 %1, i64* %4, align 8
  store %struct._mini_linkedNums* null, %struct._mini_linkedNums** %7, align 8
  %9 = load i64, i64* %3, align 8
  %10 = load i64, i64* %3, align 8
  %11 = mul nsw i64 %9, %10
  store i64 %11, i64* %5, align 8
  %12 = call align 16 i8* @malloc(i64 16) #3
  %13 = bitcast i8* %12 to %struct._mini_linkedNums*
  store %struct._mini_linkedNums* %13, %struct._mini_linkedNums** %8, align 8
  %14 = load i64, i64* %5, align 8
  %15 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %8, align 8
  %16 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %15, i32 0, i32 0
  store i64 %14, i64* %16, align 8
  %17 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %8, align 8
  %18 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %17, i32 0, i32 1
  store %struct._mini_linkedNums* null, %struct._mini_linkedNums** %18, align 8
  %19 = load i64, i64* %4, align 8
  %20 = sub nsw i64 %19, 1
  store i64 %20, i64* %4, align 8
  %21 = load i64, i64* %5, align 8
  store i64 %21, i64* %6, align 8
  br label %22

22:                                               ; preds = %25, %2
  %23 = load i64, i64* %4, align 8
  %24 = icmp sgt i64 %23, 0
  br i1 %24, label %25, label %52

25:                                               ; preds = %22
  %26 = load i64, i64* %6, align 8
  %27 = load i64, i64* %6, align 8
  %28 = mul nsw i64 %26, %27
  %29 = load i64, i64* %3, align 8
  %30 = sdiv i64 %28, %29
  %31 = load i64, i64* %3, align 8
  %32 = sdiv i64 %31, 2
  %33 = mul nsw i64 %30, %32
  %34 = add nsw i64 %33, 1
  store i64 %34, i64* %5, align 8
  %35 = load i64, i64* %5, align 8
  %36 = load i64, i64* %5, align 8
  %37 = sdiv i64 %36, 1000000000
  %38 = mul nsw i64 %37, 1000000000
  %39 = sub nsw i64 %35, %38
  store i64 %39, i64* %5, align 8
  %40 = call align 16 i8* @malloc(i64 16) #3
  %41 = bitcast i8* %40 to %struct._mini_linkedNums*
  store %struct._mini_linkedNums* %41, %struct._mini_linkedNums** %7, align 8
  %42 = load i64, i64* %5, align 8
  %43 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %7, align 8
  %44 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %43, i32 0, i32 0
  store i64 %42, i64* %44, align 8
  %45 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %8, align 8
  %46 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %7, align 8
  %47 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %46, i32 0, i32 1
  store %struct._mini_linkedNums* %45, %struct._mini_linkedNums** %47, align 8
  %48 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %7, align 8
  store %struct._mini_linkedNums* %48, %struct._mini_linkedNums** %8, align 8
  %49 = load i64, i64* %4, align 8
  %50 = sub nsw i64 %49, 1
  store i64 %50, i64* %4, align 8
  %51 = load i64, i64* %5, align 8
  store i64 %51, i64* %6, align 8
  br label %22, !llvm.loop !5

52:                                               ; preds = %22
  %53 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %7, align 8
  ret %struct._mini_linkedNums* %53
}

; Function Attrs: allocsize(0)
declare align 16 i8* @malloc(i64) #1

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_calcMean(%struct._mini_linkedNums* %0) #0 {
  %2 = alloca %struct._mini_linkedNums*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  store %struct._mini_linkedNums* %0, %struct._mini_linkedNums** %2, align 8
  store i64 0, i64* %3, align 8
  store i64 0, i64* %4, align 8
  store i64 0, i64* %5, align 8
  br label %6

6:                                                ; preds = %9, %1
  %7 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %8 = icmp ne %struct._mini_linkedNums* %7, null
  br i1 %8, label %9, label %20

9:                                                ; preds = %6
  %10 = load i64, i64* %4, align 8
  %11 = add nsw i64 %10, 1
  store i64 %11, i64* %4, align 8
  %12 = load i64, i64* %3, align 8
  %13 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %14 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %13, i32 0, i32 0
  %15 = load i64, i64* %14, align 8
  %16 = add nsw i64 %12, %15
  store i64 %16, i64* %3, align 8
  %17 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %18 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %17, i32 0, i32 1
  %19 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %18, align 8
  store %struct._mini_linkedNums* %19, %struct._mini_linkedNums** %2, align 8
  br label %6, !llvm.loop !7

20:                                               ; preds = %6
  %21 = load i64, i64* %4, align 8
  %22 = icmp ne i64 %21, 0
  br i1 %22, label %23, label %27

23:                                               ; preds = %20
  %24 = load i64, i64* %3, align 8
  %25 = load i64, i64* %4, align 8
  %26 = sdiv i64 %24, %25
  store i64 %26, i64* %5, align 8
  br label %27

27:                                               ; preds = %23, %20
  %28 = load i64, i64* %5, align 8
  ret i64 %28
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_approxSqrt(i64 %0) #0 {
  %2 = alloca i64, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  store i64 %0, i64* %2, align 8
  store i64 1, i64* %3, align 8
  %6 = load i64, i64* %3, align 8
  store i64 %6, i64* %5, align 8
  store i64 0, i64* %4, align 8
  br label %7

7:                                                ; preds = %11, %1
  %8 = load i64, i64* %4, align 8
  %9 = load i64, i64* %2, align 8
  %10 = icmp slt i64 %8, %9
  br i1 %10, label %11, label %18

11:                                               ; preds = %7
  %12 = load i64, i64* %3, align 8
  %13 = load i64, i64* %3, align 8
  %14 = mul nsw i64 %12, %13
  store i64 %14, i64* %4, align 8
  %15 = load i64, i64* %3, align 8
  store i64 %15, i64* %5, align 8
  %16 = load i64, i64* %3, align 8
  %17 = add nsw i64 %16, 1
  store i64 %17, i64* %3, align 8
  br label %7, !llvm.loop !8

18:                                               ; preds = %7
  %19 = load i64, i64* %5, align 8
  ret i64 %19
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_mini_approxSqrtAll(%struct._mini_linkedNums* %0) #0 {
  %2 = alloca %struct._mini_linkedNums*, align 8
  store %struct._mini_linkedNums* %0, %struct._mini_linkedNums** %2, align 8
  br label %3

3:                                                ; preds = %6, %1
  %4 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %5 = icmp ne %struct._mini_linkedNums* %4, null
  br i1 %5, label %6, label %15

6:                                                ; preds = %3
  %7 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %8 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %7, i32 0, i32 0
  %9 = load i64, i64* %8, align 8
  %10 = call i64 @_mini_approxSqrt(i64 %9)
  %11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), i64 %10)
  %12 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %13 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %12, i32 0, i32 1
  %14 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %13, align 8
  store %struct._mini_linkedNums* %14, %struct._mini_linkedNums** %2, align 8
  br label %3, !llvm.loop !9

15:                                               ; preds = %3
  ret void
}

declare i32 @printf(i8*, ...) #2

; Function Attrs: noinline nounwind optnone ssp uwtable
define void @_mini_range(%struct._mini_linkedNums* %0) #0 {
  %2 = alloca %struct._mini_linkedNums*, align 8
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  store %struct._mini_linkedNums* %0, %struct._mini_linkedNums** %2, align 8
  store i64 0, i64* %3, align 8
  store i64 0, i64* %4, align 8
  store i64 1, i64* %5, align 8
  br label %6

6:                                                ; preds = %41, %1
  %7 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %8 = icmp ne %struct._mini_linkedNums* %7, null
  br i1 %8, label %9, label %45

9:                                                ; preds = %6
  %10 = load i64, i64* %5, align 8
  %11 = icmp ne i64 %10, 0
  br i1 %11, label %12, label %19

12:                                               ; preds = %9
  %13 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %14 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %13, i32 0, i32 0
  %15 = load i64, i64* %14, align 8
  store i64 %15, i64* %3, align 8
  %16 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %17 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %16, i32 0, i32 0
  %18 = load i64, i64* %17, align 8
  store i64 %18, i64* %4, align 8
  store i64 0, i64* %5, align 8
  br label %41

19:                                               ; preds = %9
  %20 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %21 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %20, i32 0, i32 0
  %22 = load i64, i64* %21, align 8
  %23 = load i64, i64* %3, align 8
  %24 = icmp slt i64 %22, %23
  br i1 %24, label %25, label %29

25:                                               ; preds = %19
  %26 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %27 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %26, i32 0, i32 0
  %28 = load i64, i64* %27, align 8
  store i64 %28, i64* %3, align 8
  br label %40

29:                                               ; preds = %19
  %30 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %31 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %30, i32 0, i32 0
  %32 = load i64, i64* %31, align 8
  %33 = load i64, i64* %4, align 8
  %34 = icmp sgt i64 %32, %33
  br i1 %34, label %35, label %39

35:                                               ; preds = %29
  %36 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %37 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %36, i32 0, i32 0
  %38 = load i64, i64* %37, align 8
  store i64 %38, i64* %4, align 8
  br label %39

39:                                               ; preds = %35, %29
  br label %40

40:                                               ; preds = %39, %25
  br label %41

41:                                               ; preds = %40, %12
  %42 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %2, align 8
  %43 = getelementptr inbounds %struct._mini_linkedNums, %struct._mini_linkedNums* %42, i32 0, i32 1
  %44 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %43, align 8
  store %struct._mini_linkedNums* %44, %struct._mini_linkedNums** %2, align 8
  br label %6, !llvm.loop !10

45:                                               ; preds = %6
  %46 = load i64, i64* %3, align 8
  %47 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), i64 %46)
  %48 = load i64, i64* %4, align 8
  %49 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), i64 %48)
  ret void
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_main() #0 {
  %1 = alloca i64, align 8
  %2 = alloca i64, align 8
  %3 = alloca i64, align 8
  %4 = alloca %struct._mini_linkedNums*, align 8
  %5 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i64* %1)
  %6 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i64* %2)
  %7 = load i64, i64* %1, align 8
  %8 = load i64, i64* %2, align 8
  %9 = call %struct._mini_linkedNums* @_mini_getRands(i64 %7, i64 %8)
  store %struct._mini_linkedNums* %9, %struct._mini_linkedNums** %4, align 8
  %10 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %4, align 8
  %11 = call i64 @_mini_calcMean(%struct._mini_linkedNums* %10)
  store i64 %11, i64* %3, align 8
  %12 = load i64, i64* %3, align 8
  %13 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str, i64 0, i64 0), i64 %12)
  %14 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %4, align 8
  call void @_mini_range(%struct._mini_linkedNums* %14)
  %15 = load %struct._mini_linkedNums*, %struct._mini_linkedNums** %4, align 8
  call void @_mini_approxSqrtAll(%struct._mini_linkedNums* %15)
  ret i64 0
}

declare i32 @scanf(i8*, ...) #2

; Function Attrs: noinline nounwind optnone ssp uwtable
define i32 @main() #0 {
  %1 = alloca i32, align 4
  store i32 0, i32* %1, align 4
  %2 = call i64 @_mini_main()
  %3 = trunc i64 %2 to i32
  ret i32 %3
}

attributes #0 = { noinline nounwind optnone ssp uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #1 = { allocsize(0) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #2 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }
attributes #3 = { allocsize(0) }

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
!9 = distinct !{!9, !6}
!10 = distinct !{!10, !6}
