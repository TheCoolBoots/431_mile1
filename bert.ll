target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.node = type {i32, %struct.node*}
%struct.tnode = type {i32, %struct.tnode*, %struct.tnode*}
%struct.i = type {i32}
%struct.myCopy = type {i32}
@a = common dso_local global i32 0
@b = common dso_local global i32 0
@i = common dso_local global %struct.i* null
define %struct.node* @concatLists(%struct.node* %first, %struct.node* %second) {
l1:
br label %l2
l2:
%t7 = icmp eq %struct.node* %first, null
br i1 %t7, label %l3, label %l4
l3:
ret %struct.node* %second
l4:
br label %l5
l5:
%t6 = phi %struct.node* [%t6, %l6], [%first, %l4]
%t4 = phi %struct.node* [%t4, %l6], [%second, %l4]
%t1 = phi %struct.node* [%t3, %l6], [%first, %l4]
%t8 = getelementptr %struct.node, %struct.node* %t1, i32 0, i32 1
%t9 = load %struct.node*, %struct.node** %t8
%t10 = icmp ne %struct.node* %t9, null
br i1 %t10, label %l6, label %l7
l6:
%t2 = getelementptr %struct.node, %struct.node* %t1, i32 0, i32 1
%t3 = load %struct.node*, %struct.node** %t2
br label %l5
l7:
%t5 = getelementptr %struct.node, %struct.node* %t1, i32 0, i32 1
store %struct.node* %t4, %struct.node** %t5
ret %struct.node* %t6
}
define %struct.node* @add(%struct.node* %list, i32 %toAdd) {
l1:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.node*
%t3 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 0
store i32 %toAdd, i32* %t3
%t4 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 1
store %struct.node* %list, %struct.node** %t4
ret %struct.node* %t2
}
define i32 @size(%struct.node* %list) {
l1:
br label %l2
l2:
%t5 = icmp eq %struct.node* %list, null
br i1 %t5, label %l3, label %l4
l3:
ret i32 0
l4:
%t1 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 1
%t2 = load %struct.node*, %struct.node** %t1
%t3 = call i32 @size(%struct.node* %t2)
%t4 = add i32 1, %t3
ret i32 %t4
}
define i32 @get(%struct.node* %list, i32 %index) {
l1:
br label %l2
l2:
%t7 = icmp eq i32 %index, 0
br i1 %t7, label %l3, label %l4
l3:
%t1 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 0
%t2 = load i32, i32* %t1
ret i32 %t2
l4:
%t3 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 1
%t4 = load %struct.node*, %struct.node** %t3
%t5 = sub i32 %index, 1
%t6 = call i32 @get(%struct.node* %t4, i32 %t5)
ret i32 %t6
}
define %struct.node* @pop(%struct.node* %list) {
l1:
%t1 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 1
%t2 = load %struct.node*, %struct.node** %t1
ret %struct.node* %t2
}
define void @printList(%struct.node* %list) {
l1:
br label %l2
l2:
%t6 = icmp ne %struct.node* %list, null
br i1 %t6, label %l3, label %l4
l3:
%t1 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 0
%t2 = load i32, i32* %t1
%t3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t2)
%t4 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 1
%t5 = load %struct.node*, %struct.node** %t4
call void @printList(%struct.node* %t5)
br label %l4
l4:
ret void
}
define void @treeprint(%struct.tnode* %root) {
l1:
br label %l2
l2:
%t8 = icmp ne %struct.tnode* %root, null
br i1 %t8, label %l3, label %l4
l3:
%t1 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t2 = load %struct.tnode*, %struct.tnode** %t1
call void @treeprint(%struct.tnode* %t2)
%t3 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t4 = load i32, i32* %t3
%t5 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t4)
%t6 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t7 = load %struct.tnode*, %struct.tnode** %t6
call void @treeprint(%struct.tnode* %t7)
br label %l4
l4:
ret void
}
define void @freeList(%struct.node* %list) {
l1:
br label %l2
l2:
%t4 = icmp ne %struct.node* %list, null
br i1 %t4, label %l3, label %l4
l3:
%t1 = getelementptr %struct.node, %struct.node* %list, i32 0, i32 1
%t2 = load %struct.node*, %struct.node** %t1
call void @freeList(%struct.node* %t2)
%t3 = bitcast %struct.node* %list to i8*
call void @free(i8* %t3)
br label %l4
l4:
ret void
}
define void @freeTree(%struct.tnode* %root) {
l1:
br label %l2
l2:
%t6 = icmp eq %struct.tnode* %root, null
%t7 = xor i1 1, %t6
br i1 %t7, label %l3, label %l4
l3:
%t1 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t2 = load %struct.tnode*, %struct.tnode** %t1
call void @freeTree(%struct.tnode* %t2)
%t3 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t4 = load %struct.tnode*, %struct.tnode** %t3
call void @freeTree(%struct.tnode* %t4)
%t5 = bitcast %struct.tnode* %root to i8*
call void @free(i8* %t5)
br label %l4
l4:
ret void
}
define %struct.node* @postOrder(%struct.tnode* %root) {
l1:
br label %l2
l2:
%t15 = icmp ne %struct.tnode* %root, null
br i1 %t15, label %l3, label %l4
l3:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.node*
%t3 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t4 = load i32, i32* %t3
%t5 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 0
store i32 %t4, i32* %t5
%t6 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 1
store %struct.node* null, %struct.node** %t6
%t7 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t8 = load %struct.tnode*, %struct.tnode** %t7
%t9 = call %struct.node* @postOrder(%struct.tnode* %t8)
%t10 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t11 = load %struct.tnode*, %struct.tnode** %t10
%t12 = call %struct.node* @postOrder(%struct.tnode* %t11)
%t13 = call %struct.node* @concatLists(%struct.node* %t9, %struct.node* %t12)
%t14 = call %struct.node* @concatLists(%struct.node* %t13, %struct.node* %t2)
ret %struct.node* %t14
l4:
ret %struct.node* null
}
define %struct.tnode* @treeadd(%struct.tnode* %root, i32 %toAdd) {
l1:
br label %l2
l2:
%t15 = icmp eq %struct.tnode* %root, null
br i1 %t15, label %l3, label %l4
l3:
%t1 = call i8* @malloc(i32 12)
%t2 = bitcast i8* %t1 to %struct.tnode*
%t3 = getelementptr %struct.tnode, %struct.tnode* %t2, i32 0, i32 0
store i32 %toAdd, i32* %t3
%t4 = getelementptr %struct.tnode, %struct.tnode* %t2, i32 0, i32 1
store %struct.tnode* null, %struct.tnode** %t4
%t5 = getelementptr %struct.tnode, %struct.tnode* %t2, i32 0, i32 2
store %struct.tnode* null, %struct.tnode** %t5
ret %struct.tnode* %t2
l4:
br label %l5
l5:
%t16 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t17 = load i32, i32* %t16
%t18 = icmp slt i32 %toAdd, %t17
br i1 %t18, label %l6, label %l7
l6:
%t6 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t7 = load %struct.tnode*, %struct.tnode** %t6
%t8 = call %struct.tnode* @treeadd(%struct.tnode* %t7, i32 %toAdd)
%t9 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
store %struct.tnode* %t8, %struct.tnode** %t9
br label %l8
l7:
%t10 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t11 = load %struct.tnode*, %struct.tnode** %t10
%t12 = call %struct.tnode* @treeadd(%struct.tnode* %t11, i32 %toAdd)
%t13 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
store %struct.tnode* %t12, %struct.tnode** %t13
br label %l8
l8:
%t14 = phi %struct.tnode* [%root, %l6], [%root, %l7]
ret %struct.tnode* %t14
}
define %struct.node* @quickSort(%struct.node* %list) {
l1:
br label %l2
l2:
%t24 = call i32 @size(%struct.node* %list)
%t25 = icmp sle i32 %t24, 1
br i1 %t25, label %l3, label %l4
l3:
ret %struct.node* %list
l4:
%t1 = call i32 @get(%struct.node* %list, i32 0)
%t2 = call i32 @size(%struct.node* %list)
%t3 = sub i32 %t2, 1
%t4 = call i32 @get(%struct.node* %list, i32 %t3)
%t5 = add i32 %t1, %t4
%t6 = sdiv i32 %t5, 2
br label %l5
l5:
%t28 = phi i32 [%t30, %l10], [%t6, %l4]
%t15 = phi %struct.node* [%t18, %l10], [%list, %l4]
%t12 = phi %struct.node* [%t31, %l10], [null, %l4]
%t9 = phi i32 [%t20, %l10], [0, %l4]
%t8 = phi %struct.node* [%t32, %l10], [%list, %l4]
%t7 = phi %struct.node* [%t33, %l10], [null, %l4]
%t26 = icmp ne %struct.node* %t15, null
br i1 %t26, label %l6, label %l11
l6:
br label %l7
l7:
%t27 = call i32 @get(%struct.node* %t8, i32 %t9)
%t29 = icmp sgt i32 %t27, %t28
br i1 %t29, label %l8, label %l9
l8:
%t10 = call i32 @get(%struct.node* %t8, i32 %t9)
%t11 = call %struct.node* @add(null %t7, i32 %t10)
br label %l10
l9:
%t13 = call i32 @get(%struct.node* %t8, i32 %t9)
%t14 = call %struct.node* @add(null %t12, i32 %t13)
br label %l10
l10:
%t33 = phi %struct.node* [%t11, %l8], [%t7, %l9]
%t32 = phi %struct.node* [%t8, %l8], [%t8, %l9]
%t31 = phi null [%t12, %l8], [%t14, %l9]
%t30 = phi i32 [%t28, %l8], [%t28, %l9]
%t19 = phi i32 [%t9, %l8], [%t9, %l9]
%t16 = phi %struct.node* [%t15, %l8], [%t15, %l9]
%t17 = getelementptr %struct.node, %struct.node* %t16, i32 0, i32 1
%t18 = load %struct.node*, %struct.node** %t17
%t20 = add i32 %t19, 1
br label %l5
l11:
call void @freeList(%struct.node* %t8)
%t21 = call %struct.node* @quickSort(null %t12)
%t22 = call %struct.node* @quickSort(null %t7)
%t23 = call %struct.node* @concatLists(%struct.node* %t21, %struct.node* %t22)
ret %struct.node* %t23
}
define %struct.node* @quickSortMain(%struct.node* %list) {
l1:
call void @printList(%struct.node* %list)
%t1 = mul i32 -1, 999
%t2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t1)
call void @printList(%struct.node* %list)
%t3 = mul i32 -1, 999
%t4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t3)
call void @printList(%struct.node* %list)
%t5 = mul i32 -1, 999
%t6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t5)
ret %struct.node* null
}
define i32 @treesearch(%struct.tnode* %root, i32 %target) {
l1:
%t1 = mul i32 -1, 1
%t2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t1)
br label %l2
l2:
%t3 = icmp ne %struct.tnode* %root, null
br i1 %t3, label %l3, label %l14
l3:
br label %l4
l4:
%t4 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t5 = load i32, i32* %t4
%t6 = icmp eq i32 %t5, %target
br i1 %t6, label %l5, label %l6
l5:
ret i32 1
l6:
br label %l7
l7:
%t7 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t8 = load %struct.tnode*, %struct.tnode** %t7
%t9 = call i32 @treesearch(%struct.tnode* %t8, i32 %target)
%t10 = icmp eq i32 %t9, 1
br i1 %t10, label %l8, label %l9
l8:
ret i32 1
l9:
br label %l10
l10:
%t11 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t12 = load %struct.tnode*, %struct.tnode** %t11
%t13 = call i32 @treesearch(%struct.tnode* %t12, i32 %target)
%t14 = icmp eq i32 %t13, 1
br i1 %t14, label %l11, label %l12
l11:
ret i32 1
l12:
ret i32 0
l14:
ret i32 0
}
define %struct.node* @inOrder(%struct.tnode* %root) {
l1:
br label %l2
l2:
%t15 = icmp ne %struct.tnode* %root, null
br i1 %t15, label %l3, label %l4
l3:
%t1 = call i8* @malloc(i32 8)
%t2 = bitcast i8* %t1 to %struct.node*
%t3 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t4 = load i32, i32* %t3
%t5 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 0
store i32 %t4, i32* %t5
%t6 = getelementptr %struct.node, %struct.node* %t2, i32 0, i32 1
store %struct.node* null, %struct.node** %t6
%t7 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t8 = load %struct.tnode*, %struct.tnode** %t7
%t9 = call %struct.node* @inOrder(%struct.tnode* %t8)
%t10 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t11 = load %struct.tnode*, %struct.tnode** %t10
%t12 = call %struct.node* @inOrder(%struct.tnode* %t11)
%t13 = call %struct.node* @concatLists(%struct.node* %t2, %struct.node* %t12)
%t14 = call %struct.node* @concatLists(%struct.node* %t9, %struct.node* %t13)
ret %struct.node* %t14
l4:
ret %struct.node* null
}
define i32 @bintreesearch(%struct.tnode* %root, i32 %target) {
l1:
%t1 = mul i32 -1, 1
%t2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t1)
br label %l2
l2:
%t9 = icmp ne %struct.tnode* %root, null
br i1 %t9, label %l3, label %l11
l3:
br label %l4
l4:
%t10 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t11 = load i32, i32* %t10
%t12 = icmp eq i32 %t11, %target
br i1 %t12, label %l5, label %l6
l5:
ret i32 1
l6:
br label %l7
l7:
%t13 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 0
%t14 = load i32, i32* %t13
%t15 = icmp slt i32 %target, %t14
br i1 %t15, label %l8, label %l9
l8:
%t3 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 1
%t4 = load %struct.tnode*, %struct.tnode** %t3
%t5 = call i32 @bintreesearch(%struct.tnode* %t4, i32 %target)
ret i32 %t5
l9:
%t6 = getelementptr %struct.tnode, %struct.tnode* %root, i32 0, i32 2
%t7 = load %struct.tnode*, %struct.tnode** %t6
%t8 = call i32 @bintreesearch(%struct.tnode* %t7, i32 %target)
ret i32 %t8
l11:
ret i32 0
}
define %struct.tnode* @buildTree(%struct.node* %list) {
l1:
br label %l2
l2:
%t3 = phi i32 [%t6, %l3], [0, %l1]
%t2 = phi %struct.node* [%t2, %l3], [%list, %l1]
%t1 = phi %struct.tnode* [%t5, %l3], [null, %l1]
%t7 = call i32 @size(%struct.node* %t2)
%t8 = icmp slt i32 %t3, %t7
br i1 %t8, label %l3, label %l4
l3:
%t4 = call i32 @get(%struct.node* %t2, i32 %t3)
%t5 = call %struct.tnode* @treeadd(null %t1, i32 %t4)
%t6 = add i32 %t3, 1
br label %l2
l4:
ret %struct.tnode* %t1
}
define void @treeMain(%struct.node* %list) {
l1:
%t1 = call %struct.tnode* @buildTree(%struct.node* %list)
call void @treeprint(%struct.tnode* %t1)
%t2 = mul i32 -1, 999
%t3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t2)
%t4 = call %struct.node* @inOrder(%struct.tnode* %t1)
call void @printList(%struct.node* %t4)
%t5 = mul i32 -1, 999
%t6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t5)
call void @freeList(%struct.node* %t4)
%t7 = call %struct.node* @postOrder(%struct.tnode* %t1)
call void @printList(%struct.node* %t7)
%t8 = mul i32 -1, 999
%t9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t8)
call void @freeList(%struct.node* %t7)
%t10 = call i32 @treesearch(%struct.tnode* %t1, i32 0)
%t11 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t10)
%t12 = mul i32 -1, 999
%t13 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t12)
%t14 = call i32 @treesearch(%struct.tnode* %t1, i32 10)
%t15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t14)
%t16 = mul i32 -1, 999
%t17 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t16)
%t18 = mul i32 -1, 2
%t19 = call i32 @treesearch(%struct.tnode* %t1, i32 %t18)
%t20 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t19)
%t21 = mul i32 -1, 999
%t22 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t21)
%t23 = call i32 @treesearch(%struct.tnode* %t1, i32 2)
%t24 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t23)
%t25 = mul i32 -1, 999
%t26 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t25)
%t27 = call i32 @treesearch(%struct.tnode* %t1, i32 3)
%t28 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t27)
%t29 = mul i32 -1, 999
%t30 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t29)
%t31 = call i32 @treesearch(%struct.tnode* %t1, i32 9)
%t32 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t31)
%t33 = mul i32 -1, 999
%t34 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t33)
%t35 = call i32 @treesearch(%struct.tnode* %t1, i32 1)
%t36 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t35)
%t37 = mul i32 -1, 999
%t38 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t37)
%t39 = call i32 @bintreesearch(%struct.tnode* %t1, i32 0)
%t40 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t39)
%t41 = mul i32 -1, 999
%t42 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t41)
%t43 = call i32 @bintreesearch(%struct.tnode* %t1, i32 10)
%t44 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t43)
%t45 = mul i32 -1, 999
%t46 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t45)
%t47 = mul i32 -1, 2
%t48 = call i32 @bintreesearch(%struct.tnode* %t1, i32 %t47)
%t49 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t48)
%t50 = mul i32 -1, 999
%t51 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t50)
%t52 = call i32 @bintreesearch(%struct.tnode* %t1, i32 2)
%t53 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t52)
%t54 = mul i32 -1, 999
%t55 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t54)
%t56 = call i32 @bintreesearch(%struct.tnode* %t1, i32 3)
%t57 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t56)
%t58 = mul i32 -1, 999
%t59 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t58)
%t60 = call i32 @bintreesearch(%struct.tnode* %t1, i32 9)
%t61 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t60)
%t62 = mul i32 -1, 999
%t63 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t62)
%t64 = call i32 @bintreesearch(%struct.tnode* %t1, i32 1)
%t65 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t64)
%t66 = mul i32 -1, 999
%t67 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t66)
call void @freeTree(%struct.tnode* %t1)
ret void
}
define %struct.node* @myCopy(%struct.node* %src) {
l1:
br label %l2
l2:
%t8 = icmp eq %struct.node* %src, null
br i1 %t8, label %l3, label %l4
l3:
ret %struct.node* null
l4:
%t1 = getelementptr %struct.node, %struct.node* %src, i32 0, i32 0
%t2 = load i32, i32* %t1
%t3 = call %struct.node* @add(null null, i32 %t2)
%t4 = getelementptr %struct.node, %struct.node* %src, i32 0, i32 1
%t5 = load %struct.node*, %struct.node** %t4
%t6 = call %struct.node* @myCopy(%struct.node* %t5)
%t7 = call %struct.node* @concatLists(%struct.node* %t3, %struct.node* %t6)
ret %struct.node* %t7
}
define i32 @main() {
l1:
br label %l2
l2:
%t13 = phi i32 [%t14, %l3], [0, %l1]
%t12 = phi %struct.node* [%t11, %l3], [null, %l1]
%t10 = phi %struct.node* [%t9, %l3], [null, %l1]
%t8 = phi %struct.node* [%t7, %l3], [null, %l1]
%t5 = phi %struct.node* [%t6, %l3], [null, %l1]
%t4 = phi i32 [%t3, %l3], [0, %l1]
%t15 = icmp slt i32 %t13, 10
br i1 %t15, label %l3, label %l4
l3:
%t1 = alloca i32
%t2 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t1)
%t3 = load i32, i32* %t1
%t6 = call %struct.node* @add(null %t5, i32 %t3)
%t7 = call %struct.node* @myCopy(%struct.node* %t6)
%t9 = call %struct.node* @myCopy(%struct.node* %t6)
%t11 = call %struct.node* @quickSortMain(%struct.node* %t7)
call void @freeList(%struct.node* %t11)
call void @treeMain(%struct.node* %t9)
%t14 = add i32 %t13, 1
br label %l2
l4:
call void @freeList(null %t5)
call void @freeList(null %t8)
call void @freeList(null %t10)
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
