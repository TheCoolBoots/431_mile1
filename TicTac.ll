target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-apple-macosx10.15.0"
declare align 16 i8* @malloc(i32) #2
declare void @free(i8*) #1
declare i32 @printf(i8*, ...) #1
declare i32 @scanf(i8*, ...) #1
@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1
%struct.gameBoard = type {i32, i32, i32, i32, i32, i32, i32, i32, i32}
define void @cleanBoard(%struct.gameBoard* %board) {
l1:
%t1 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 0
store i32 0, i32* %t1
%t2 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 1
store i32 0, i32* %t2
%t3 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 2
store i32 0, i32* %t3
%t4 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 3
store i32 0, i32* %t4
%t5 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 4
store i32 0, i32* %t5
%t6 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 5
store i32 0, i32* %t6
%t7 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 6
store i32 0, i32* %t7
%t8 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 7
store i32 0, i32* %t8
%t9 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 8
store i32 0, i32* %t9
ret void
}
define void @printBoard(%struct.gameBoard* %board) {
l1:
%t1 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 0
%t2 = load i32, i32* %t1
%t3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t2)
%t4 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 1
%t5 = load i32, i32* %t4
%t6 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t5)
%t7 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 2
%t8 = load i32, i32* %t7
%t9 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t8)
%t10 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 3
%t11 = load i32, i32* %t10
%t12 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t11)
%t13 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 4
%t14 = load i32, i32* %t13
%t15 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t14)
%t16 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 5
%t17 = load i32, i32* %t16
%t18 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t17)
%t19 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 6
%t20 = load i32, i32* %t19
%t21 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t20)
%t22 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 7
%t23 = load i32, i32* %t22
%t24 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %t23)
%t25 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 8
%t26 = load i32, i32* %t25
%t27 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t26)
ret void
}
define void @printMoveBoard() {
l1:
%t1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 123)
%t2 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 456)
%t3 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 789)
ret void
}
define void @placePiece(%struct.gameBoard* %board, i32 %turn, i32 %placement) {
l1:
br label %l2
l2:
%t10 = icmp eq i32 %placement, 1
br i1 %t10, label %l3, label %l4
l3:
%t1 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 0
store i32 %turn, i32* %t1
br label %l36
l4:
br label %l5
l5:
%t11 = icmp eq i32 %placement, 2
br i1 %t11, label %l6, label %l7
l6:
%t2 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 1
store i32 %turn, i32* %t2
br label %l35
l7:
br label %l8
l8:
%t12 = icmp eq i32 %placement, 3
br i1 %t12, label %l9, label %l10
l9:
%t3 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 2
store i32 %turn, i32* %t3
br label %l34
l10:
br label %l11
l11:
%t13 = icmp eq i32 %placement, 4
br i1 %t13, label %l12, label %l13
l12:
%t4 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 3
store i32 %turn, i32* %t4
br label %l33
l13:
br label %l14
l14:
%t14 = icmp eq i32 %placement, 5
br i1 %t14, label %l15, label %l16
l15:
%t5 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 4
store i32 %turn, i32* %t5
br label %l32
l16:
br label %l17
l17:
%t15 = icmp eq i32 %placement, 6
br i1 %t15, label %l18, label %l19
l18:
%t6 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 5
store i32 %turn, i32* %t6
br label %l31
l19:
br label %l20
l20:
%t16 = icmp eq i32 %placement, 7
br i1 %t16, label %l21, label %l22
l21:
%t7 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 6
store i32 %turn, i32* %t7
br label %l30
l22:
br label %l23
l23:
%t17 = icmp eq i32 %placement, 8
br i1 %t17, label %l24, label %l25
l24:
%t8 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 7
store i32 %turn, i32* %t8
br label %l29
l25:
br label %l26
l26:
%t18 = icmp eq i32 %placement, 9
br i1 %t18, label %l27, label %l28
l27:
%t9 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 8
store i32 %turn, i32* %t9
br label %l28
l28:
br label %l29
l29:
br label %l30
l30:
br label %l31
l31:
br label %l32
l32:
br label %l33
l33:
br label %l34
l34:
br label %l35
l35:
br label %l36
l36:
ret void
}
define i32 @checkWinner(%struct.gameBoard* %board) {
l1:
br label %l2
l2:
%t2 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 0
%t3 = load i32, i32* %t2
%t4 = icmp eq i32 %t3, 1
br i1 %t4, label %l3, label %l10
l3:
br label %l4
l4:
%t5 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 1
%t6 = load i32, i32* %t5
%t7 = icmp eq i32 %t6, 1
br i1 %t7, label %l5, label %l9
l5:
br label %l6
l6:
%t8 = getelementptr %struct.gameBoard, %struct.gameBoard* %board, i32 0, i32 2
%t9 = load i32, i32* %t8
%t10 = icmp eq i32 %t9, 1
br i1 %t10, label %l7, label %l8
l7:
ret i32 0
l8:
br label %l9
l9:
%t11 = phi %struct.gameBoard* [%board, %l4], [%board, %l8]
br label %l10
l10:
%t12 = phi %struct.gameBoard* [%board, %l2], [%t11, %l9]
br label %l11
l11:
%t13 = getelementptr %struct.gameBoard, %struct.gameBoard* %t12, i32 0, i32 0
%t14 = load i32, i32* %t13
%t15 = icmp eq i32 %t14, 2
br i1 %t15, label %l12, label %l19
l12:
br label %l13
l13:
%t16 = getelementptr %struct.gameBoard, %struct.gameBoard* %t12, i32 0, i32 1
%t17 = load i32, i32* %t16
%t18 = icmp eq i32 %t17, 2
br i1 %t18, label %l14, label %l18
l14:
br label %l15
l15:
%t19 = getelementptr %struct.gameBoard, %struct.gameBoard* %t12, i32 0, i32 2
%t20 = load i32, i32* %t19
%t21 = icmp eq i32 %t20, 2
br i1 %t21, label %l16, label %l17
l16:
ret i32 1
l17:
br label %l18
l18:
%t22 = phi %struct.gameBoard* [%t12, %l13], [%t12, %l17]
br label %l19
l19:
%t23 = phi %struct.gameBoard* [%t12, %l11], [%t22, %l18]
br label %l20
l20:
%t24 = getelementptr %struct.gameBoard, %struct.gameBoard* %t23, i32 0, i32 3
%t25 = load i32, i32* %t24
%t26 = icmp eq i32 %t25, 1
br i1 %t26, label %l21, label %l28
l21:
br label %l22
l22:
%t27 = getelementptr %struct.gameBoard, %struct.gameBoard* %t23, i32 0, i32 4
%t28 = load i32, i32* %t27
%t29 = icmp eq i32 %t28, 1
br i1 %t29, label %l23, label %l27
l23:
br label %l24
l24:
%t30 = getelementptr %struct.gameBoard, %struct.gameBoard* %t23, i32 0, i32 5
%t31 = load i32, i32* %t30
%t32 = icmp eq i32 %t31, 1
br i1 %t32, label %l25, label %l26
l25:
ret i32 0
l26:
br label %l27
l27:
%t33 = phi %struct.gameBoard* [%t23, %l22], [%t23, %l26]
br label %l28
l28:
%t34 = phi %struct.gameBoard* [%t23, %l20], [%t33, %l27]
br label %l29
l29:
%t35 = getelementptr %struct.gameBoard, %struct.gameBoard* %t34, i32 0, i32 3
%t36 = load i32, i32* %t35
%t37 = icmp eq i32 %t36, 2
br i1 %t37, label %l30, label %l37
l30:
br label %l31
l31:
%t38 = getelementptr %struct.gameBoard, %struct.gameBoard* %t34, i32 0, i32 4
%t39 = load i32, i32* %t38
%t40 = icmp eq i32 %t39, 2
br i1 %t40, label %l32, label %l36
l32:
br label %l33
l33:
%t41 = getelementptr %struct.gameBoard, %struct.gameBoard* %t34, i32 0, i32 5
%t42 = load i32, i32* %t41
%t43 = icmp eq i32 %t42, 2
br i1 %t43, label %l34, label %l35
l34:
ret i32 1
l35:
br label %l36
l36:
%t44 = phi %struct.gameBoard* [%t34, %l31], [%t34, %l35]
br label %l37
l37:
%t45 = phi %struct.gameBoard* [%t34, %l29], [%t44, %l36]
br label %l38
l38:
%t46 = getelementptr %struct.gameBoard, %struct.gameBoard* %t45, i32 0, i32 6
%t47 = load i32, i32* %t46
%t48 = icmp eq i32 %t47, 1
br i1 %t48, label %l39, label %l46
l39:
br label %l40
l40:
%t49 = getelementptr %struct.gameBoard, %struct.gameBoard* %t45, i32 0, i32 7
%t50 = load i32, i32* %t49
%t51 = icmp eq i32 %t50, 1
br i1 %t51, label %l41, label %l45
l41:
br label %l42
l42:
%t52 = getelementptr %struct.gameBoard, %struct.gameBoard* %t45, i32 0, i32 8
%t53 = load i32, i32* %t52
%t54 = icmp eq i32 %t53, 1
br i1 %t54, label %l43, label %l44
l43:
ret i32 0
l44:
br label %l45
l45:
%t55 = phi %struct.gameBoard* [%t45, %l40], [%t45, %l44]
br label %l46
l46:
%t56 = phi %struct.gameBoard* [%t45, %l38], [%t55, %l45]
br label %l47
l47:
%t57 = getelementptr %struct.gameBoard, %struct.gameBoard* %t56, i32 0, i32 6
%t58 = load i32, i32* %t57
%t59 = icmp eq i32 %t58, 2
br i1 %t59, label %l48, label %l55
l48:
br label %l49
l49:
%t60 = getelementptr %struct.gameBoard, %struct.gameBoard* %t56, i32 0, i32 7
%t61 = load i32, i32* %t60
%t62 = icmp eq i32 %t61, 2
br i1 %t62, label %l50, label %l54
l50:
br label %l51
l51:
%t63 = getelementptr %struct.gameBoard, %struct.gameBoard* %t56, i32 0, i32 8
%t64 = load i32, i32* %t63
%t65 = icmp eq i32 %t64, 2
br i1 %t65, label %l52, label %l53
l52:
ret i32 1
l53:
br label %l54
l54:
%t66 = phi %struct.gameBoard* [%t56, %l49], [%t56, %l53]
br label %l55
l55:
%t67 = phi %struct.gameBoard* [%t56, %l47], [%t66, %l54]
br label %l56
l56:
%t68 = getelementptr %struct.gameBoard, %struct.gameBoard* %t67, i32 0, i32 0
%t69 = load i32, i32* %t68
%t70 = icmp eq i32 %t69, 1
br i1 %t70, label %l57, label %l64
l57:
br label %l58
l58:
%t71 = getelementptr %struct.gameBoard, %struct.gameBoard* %t67, i32 0, i32 3
%t72 = load i32, i32* %t71
%t73 = icmp eq i32 %t72, 1
br i1 %t73, label %l59, label %l63
l59:
br label %l60
l60:
%t74 = getelementptr %struct.gameBoard, %struct.gameBoard* %t67, i32 0, i32 6
%t75 = load i32, i32* %t74
%t76 = icmp eq i32 %t75, 1
br i1 %t76, label %l61, label %l62
l61:
ret i32 0
l62:
br label %l63
l63:
%t77 = phi %struct.gameBoard* [%t67, %l58], [%t67, %l62]
br label %l64
l64:
%t78 = phi %struct.gameBoard* [%t67, %l56], [%t77, %l63]
br label %l65
l65:
%t79 = getelementptr %struct.gameBoard, %struct.gameBoard* %t78, i32 0, i32 0
%t80 = load i32, i32* %t79
%t81 = icmp eq i32 %t80, 2
br i1 %t81, label %l66, label %l73
l66:
br label %l67
l67:
%t82 = getelementptr %struct.gameBoard, %struct.gameBoard* %t78, i32 0, i32 3
%t83 = load i32, i32* %t82
%t84 = icmp eq i32 %t83, 2
br i1 %t84, label %l68, label %l72
l68:
br label %l69
l69:
%t85 = getelementptr %struct.gameBoard, %struct.gameBoard* %t78, i32 0, i32 6
%t86 = load i32, i32* %t85
%t87 = icmp eq i32 %t86, 2
br i1 %t87, label %l70, label %l71
l70:
ret i32 1
l71:
br label %l72
l72:
%t88 = phi %struct.gameBoard* [%t78, %l67], [%t78, %l71]
br label %l73
l73:
%t89 = phi %struct.gameBoard* [%t78, %l65], [%t88, %l72]
br label %l74
l74:
%t90 = getelementptr %struct.gameBoard, %struct.gameBoard* %t89, i32 0, i32 1
%t91 = load i32, i32* %t90
%t92 = icmp eq i32 %t91, 1
br i1 %t92, label %l75, label %l82
l75:
br label %l76
l76:
%t93 = getelementptr %struct.gameBoard, %struct.gameBoard* %t89, i32 0, i32 4
%t94 = load i32, i32* %t93
%t95 = icmp eq i32 %t94, 1
br i1 %t95, label %l77, label %l81
l77:
br label %l78
l78:
%t96 = getelementptr %struct.gameBoard, %struct.gameBoard* %t89, i32 0, i32 7
%t97 = load i32, i32* %t96
%t98 = icmp eq i32 %t97, 1
br i1 %t98, label %l79, label %l80
l79:
ret i32 0
l80:
br label %l81
l81:
%t99 = phi %struct.gameBoard* [%t89, %l76], [%t89, %l80]
br label %l82
l82:
%t100 = phi %struct.gameBoard* [%t89, %l74], [%t99, %l81]
br label %l83
l83:
%t101 = getelementptr %struct.gameBoard, %struct.gameBoard* %t100, i32 0, i32 1
%t102 = load i32, i32* %t101
%t103 = icmp eq i32 %t102, 2
br i1 %t103, label %l84, label %l91
l84:
br label %l85
l85:
%t104 = getelementptr %struct.gameBoard, %struct.gameBoard* %t100, i32 0, i32 4
%t105 = load i32, i32* %t104
%t106 = icmp eq i32 %t105, 2
br i1 %t106, label %l86, label %l90
l86:
br label %l87
l87:
%t107 = getelementptr %struct.gameBoard, %struct.gameBoard* %t100, i32 0, i32 7
%t108 = load i32, i32* %t107
%t109 = icmp eq i32 %t108, 2
br i1 %t109, label %l88, label %l89
l88:
ret i32 1
l89:
br label %l90
l90:
%t110 = phi %struct.gameBoard* [%t100, %l85], [%t100, %l89]
br label %l91
l91:
%t111 = phi %struct.gameBoard* [%t100, %l83], [%t110, %l90]
br label %l92
l92:
%t112 = getelementptr %struct.gameBoard, %struct.gameBoard* %t111, i32 0, i32 2
%t113 = load i32, i32* %t112
%t114 = icmp eq i32 %t113, 1
br i1 %t114, label %l93, label %l100
l93:
br label %l94
l94:
%t115 = getelementptr %struct.gameBoard, %struct.gameBoard* %t111, i32 0, i32 5
%t116 = load i32, i32* %t115
%t117 = icmp eq i32 %t116, 1
br i1 %t117, label %l95, label %l99
l95:
br label %l96
l96:
%t118 = getelementptr %struct.gameBoard, %struct.gameBoard* %t111, i32 0, i32 8
%t119 = load i32, i32* %t118
%t120 = icmp eq i32 %t119, 1
br i1 %t120, label %l97, label %l98
l97:
ret i32 0
l98:
br label %l99
l99:
%t121 = phi %struct.gameBoard* [%t111, %l94], [%t111, %l98]
br label %l100
l100:
%t122 = phi %struct.gameBoard* [%t111, %l92], [%t121, %l99]
br label %l101
l101:
%t123 = getelementptr %struct.gameBoard, %struct.gameBoard* %t122, i32 0, i32 2
%t124 = load i32, i32* %t123
%t125 = icmp eq i32 %t124, 2
br i1 %t125, label %l102, label %l109
l102:
br label %l103
l103:
%t126 = getelementptr %struct.gameBoard, %struct.gameBoard* %t122, i32 0, i32 5
%t127 = load i32, i32* %t126
%t128 = icmp eq i32 %t127, 2
br i1 %t128, label %l104, label %l108
l104:
br label %l105
l105:
%t129 = getelementptr %struct.gameBoard, %struct.gameBoard* %t122, i32 0, i32 8
%t130 = load i32, i32* %t129
%t131 = icmp eq i32 %t130, 2
br i1 %t131, label %l106, label %l107
l106:
ret i32 1
l107:
br label %l108
l108:
br label %l109
l109:
%t1 = mul i32 -1, 1
ret i32 %t1
}
define i32 @main() {
l1:
%t1 = mul i32 -1, 1
%t2 = call i8* @malloc(i32 36)
%t3 = bitcast i8* %t2 to %struct.gameBoard*
call void @cleanBoard(%struct.gameBoard* %t3)
br label %l2
l2:
%t4 = phi %struct.gameBoard* [%t16, %l7], [%t3, %l1]
%t5 = phi i32 [%t29, %l7], [0, %l1]
%t10 = phi i32 [%t30, %l7], [0, %l1]
%t15 = phi i32 [%t31, %l7], [0, %l1]
%t18 = phi i32 [%t17, %l7], [%t1, %l1]
%t20 = phi i32 [%t22, %l7], [0, %l1]
%t25 = icmp slt i32 %t18, 0
%t26 = icmp ne i32 %t20, 8
%t27 = and i1 %t25, %t26
br i1 %t27, label %l3, label %l8
l3:
call void @printBoard(%struct.gameBoard* %t4)
br label %l4
l4:
%t28 = icmp eq i32 %t5, 0
br i1 %t28, label %l5, label %l6
l5:
%t6 = add i32 %t5, 1
%t7 = alloca i32
%t8 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t7)
%t9 = load i32, i32* %t7
call void @placePiece(%struct.gameBoard* %t4, i32 1, i32 %t9)
br label %l7
l6:
%t11 = sub i32 %t5, 1
%t12 = alloca i32
%t13 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t12)
%t14 = load i32, i32* %t12
call void @placePiece(%struct.gameBoard* %t4, i32 2, i32 %t14)
br label %l7
l7:
%t31 = phi i32 [%t15, %l5], [%t14, %l6]
%t30 = phi i32 [%t9, %l5], [%t10, %l6]
%t29 = phi i32 [%t6, %l5], [%t11, %l6]
%t21 = phi i32 [%t20, %l5], [%t20, %l6]
%t19 = phi i32 [%t18, %l5], [%t18, %l6]
%t16 = phi %struct.gameBoard* [%t4, %l5], [%t4, %l6]
%t17 = call i32 @checkWinner(%struct.gameBoard* %t16)
%t22 = add i32 %t21, 1
br label %l2
l8:
%t23 = add i32 %t18, 1
%t24 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 %t23)
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
