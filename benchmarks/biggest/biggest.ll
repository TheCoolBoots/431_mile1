; ModuleID = 'biggest.bc'
source_filename = "biggest.c"
target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"

%struct._mini_IntList = type { i64, %struct._mini_IntList* }

@.str = private unnamed_addr constant [4 x i8] c"%ld\00", align 1
@.str.1 = private unnamed_addr constant [5 x i8] c"%ld\0A\00", align 1

; Function Attrs: noinline nounwind optnone ssp uwtable
define %struct._mini_IntList* @_mini_getIntList() #0 {
  %1 = alloca %struct._mini_IntList*, align 8
  %2 = alloca %struct._mini_IntList*, align 8
  %3 = alloca i64, align 8
  %4 = call align 16 i8* @malloc(i64 16) #3
  %5 = bitcast i8* %4 to %struct._mini_IntList*
  store %struct._mini_IntList* %5, %struct._mini_IntList** %2, align 8
  %6 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str, i64 0, i64 0), i64* %3)
  %7 = load i64, i64* %3, align 8
  %8 = icmp eq i64 %7, -1
  br i1 %8, label %9, label %16

9:                                                ; preds = %0
  %10 = load i64, i64* %3, align 8
  %11 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %12 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %11, i32 0, i32 0
  store i64 %10, i64* %12, align 8
  %13 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %14 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %13, i32 0, i32 1
  store %struct._mini_IntList* null, %struct._mini_IntList** %14, align 8
  %15 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  store %struct._mini_IntList* %15, %struct._mini_IntList** %1, align 8
  br label %24

16:                                               ; preds = %0
  %17 = load i64, i64* %3, align 8
  %18 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %19 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %18, i32 0, i32 0
  store i64 %17, i64* %19, align 8
  %20 = call %struct._mini_IntList* @_mini_getIntList()
  %21 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %22 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %21, i32 0, i32 1
  store %struct._mini_IntList* %20, %struct._mini_IntList** %22, align 8
  %23 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  store %struct._mini_IntList* %23, %struct._mini_IntList** %1, align 8
  br label %24

24:                                               ; preds = %16, %9
  %25 = load %struct._mini_IntList*, %struct._mini_IntList** %1, align 8
  ret %struct._mini_IntList* %25
}

; Function Attrs: allocsize(0)
declare align 16 i8* @malloc(i64) #1

declare i32 @scanf(i8*, ...) #2

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_biggest(i64 %0, i64 %1) #0 {
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  %5 = alloca i64, align 8
  store i64 %0, i64* %4, align 8
  store i64 %1, i64* %5, align 8
  %6 = load i64, i64* %4, align 8
  %7 = load i64, i64* %5, align 8
  %8 = icmp sgt i64 %6, %7
  br i1 %8, label %9, label %11

9:                                                ; preds = %2
  %10 = load i64, i64* %4, align 8
  store i64 %10, i64* %3, align 8
  br label %13

11:                                               ; preds = %2
  %12 = load i64, i64* %5, align 8
  store i64 %12, i64* %3, align 8
  br label %13

13:                                               ; preds = %11, %9
  %14 = load i64, i64* %3, align 8
  ret i64 %14
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_biggestInList(%struct._mini_IntList* %0) #0 {
  %2 = alloca %struct._mini_IntList*, align 8
  %3 = alloca i64, align 8
  store %struct._mini_IntList* %0, %struct._mini_IntList** %2, align 8
  %4 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %5 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %4, i32 0, i32 0
  %6 = load i64, i64* %5, align 8
  store i64 %6, i64* %3, align 8
  br label %7

7:                                                ; preds = %12, %1
  %8 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %9 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %8, i32 0, i32 1
  %10 = load %struct._mini_IntList*, %struct._mini_IntList** %9, align 8
  %11 = icmp ne %struct._mini_IntList* %10, null
  br i1 %11, label %12, label %21

12:                                               ; preds = %7
  %13 = load i64, i64* %3, align 8
  %14 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %15 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %14, i32 0, i32 0
  %16 = load i64, i64* %15, align 8
  %17 = call i64 @_mini_biggest(i64 %13, i64 %16)
  store i64 %17, i64* %3, align 8
  %18 = load %struct._mini_IntList*, %struct._mini_IntList** %2, align 8
  %19 = getelementptr inbounds %struct._mini_IntList, %struct._mini_IntList* %18, i32 0, i32 1
  %20 = load %struct._mini_IntList*, %struct._mini_IntList** %19, align 8
  store %struct._mini_IntList* %20, %struct._mini_IntList** %2, align 8
  br label %7, !llvm.loop !5

21:                                               ; preds = %7
  %22 = load i64, i64* %3, align 8
  ret i64 %22
}

; Function Attrs: noinline nounwind optnone ssp uwtable
define i64 @_mini_main() #0 {
  %1 = alloca %struct._mini_IntList*, align 8
  %2 = call %struct._mini_IntList* @_mini_getIntList()
  store %struct._mini_IntList* %2, %struct._mini_IntList** %1, align 8
  %3 = load %struct._mini_IntList*, %struct._mini_IntList** %1, align 8
  %4 = call i64 @_mini_biggestInList(%struct._mini_IntList* %3)
  %5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([5 x i8], [5 x i8]* @.str.1, i64 0, i64 0), i64 %4)
  ret i64 0
}

declare i32 @printf(i8*, ...) #2

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
