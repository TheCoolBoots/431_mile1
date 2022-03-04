define i32 @main() {
l1:
%t2 = icmp sgt i32 5, 2
br i32 %t2, label %l2, label %l3
l2:
%t3 = add i32 %t1, 5
br label %l4
l3:
%t4 = add i32 %t1, 0
l4:
%t5 = phi i32 [%t3, %l2], [%t4, %l3]
ret i32 %t5
}