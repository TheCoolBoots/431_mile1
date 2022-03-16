define i32 @main() {
l1:
l2:
%t1 = phi i32 [%t3, %l3], [3, %l1]
%t2 = icmp sgt i32 %t1, 2
br i32 %t2, label %l3, label %l4
l3:
%t3 = add i32 %t1, 5
br label %l2
l4:
%t0 = add i32 %t1, 0
br label %retLabel
retLabel:
ret i32 %t0
}