; ModuleID = 'PLACEHOLDER_NAME.bc'
source_filename = "PLACEHOLDER_NAME.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"
declare i8* @malloc(i32)
declare void @free(i8*)
declare i32 @printf(i8*, i32)
declare i32 @scanf(i8*, i32*)
%
c
h
e
c
k
 
=
 
a
l
l
o
c
a
 
i
3
2


d
e
f
i
n
e
 
i
3
2
 
@
m
a
i
n
(
)
 
{


e
n
t
r
y
:


s
t
o
r
e
 
i
3
2
 
0
,
 
i
3
2
*
 
%
c
h
e
c
k


%
1
 
=
 
l
o
a
d
 
i
3
2
,
 
i
3
2
*
 
%
c
h
e
c
k


%
2
 
=
 
i
c
m
p
 
s
l
t
 
i
3
2
 
%
1
,
 
1
0
0
0
0
0


3
:


b
r
 
i
3
2
 
%
2
,
 
l
a
b
e
l
 
%
4
,
 
l
a
b
e
l
 
%
5


4
:


%
6
 
=
 
l
o
a
d
 
i
3
2
,
 
i
3
2
*
 
%
c
h
e
c
k


%
7
 
=
 
i
c
m
p
 
s
l
t
 
i
3
2
 
%
6
,
 
5
0
0
0
0


b
r
 
i
3
2
 
%
7
,
 
l
a
b
e
l
 
%
8
,
 
l
a
b
e
l
 
%
9


8
:


%
1
1
 
=
 
c
a
l
l
 
i
3
2
 
@
p
r
i
n
t
f
(
"
%
d
"
,
 
1
)


b
r
 
l
a
b
e
l
 
%
1
0


9
:


%
1
2
 
=
 
c
a
l
l
 
i
3
2
 
@
p
r
i
n
t
f
(
"
%
d
"
,
 
2
)


b
r
 
l
a
b
e
l
 
%
1
0


1
0
:


%
1
3
 
=
 
l
o
a
d
 
i
3
2
,
 
i
3
2
*
 
%
c
h
e
c
k


%
1
4
 
=
 
a
d
d
 
i
3
2
 
%
1
3
,
 
1


s
t
o
r
e
 
i
3
2
 
%
1
4
,
 
i
3
2
*
 
%
c
h
e
c
k


b
r
 
l
a
b
e
l
 
%
3


5
:


%
1
5
 
=
 
l
o
a
d
 
i
3
2
,
 
i
3
2
*
 
%
c
h
e
c
k


r
e
t
 
i
3
2
 
%
1
5


}
attributes  # 0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
!llvm.module.flags = !{!0}
!llvm.ident = !{!1}
!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 10.0.0-4ubuntu1 "}
