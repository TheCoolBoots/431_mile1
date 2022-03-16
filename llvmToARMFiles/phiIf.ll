define i32 @main() {
l1:
%t1 = add i32 3, 7
%t2 = icmp sgt i32 5, 2
br i32 %t2, label %l2, label %l3
l2:
%t3 = add i32 %t1, 5
l3:
%t4 = phi i32 [%t1, %l1], [%t3, %l2]
ret i32 %t4
}