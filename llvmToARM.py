def llvmToArm(llvmCode:list[str]) -> list[str]:
    # binop 1: target = operator i32 op1, op2
        # op1 == int?
        # op2 == int?
        # operator == 'sdiv'?
    # binop 2: target = icmp operator i32 op1, op2 
        # op1 == int?
        # op2 == int?
    # branch 1: br i32 op, label %l_, label %l_
        # op == int?
    # br2: br label %l_
    # getelptr: target = getelementptr structPtr structReg, i32 0, i32 n
    # load: target = load typePtr %t#
    # bitcast: target = bitcast typePtr src to targetType
    # funCall: target = call retType @funlabel(*(paramType paramReg))
    # alloca: %t# = alloca type
    for line in llvmCode:
        match line.split(' '):
            case [target, '=', operator, 'i32', op1, op2]:
                pass
            case [target, '=', 'icmp', operator, 'i32', op1, op2]:
                pass
            case ['br', 'i32', operand, 'label', label1, 'label', label2]:
                pass
            case ['br', 'label', label]:
                pass
            case [target, '=', 'getelementptr', structPtr, structReg, 'i32', '0', 'i32', n]:
                pass
            case [target, '=', 'load', typePtr, reg]:
                pass
            case [target, '=', 'bitcast', srcType, srcReg, 'to', targetType]:
                pass
            case [target, '=', 'call', retType, *rest]:
                pass
            case [target, '=', 'alloca', type]:
                pass
    pass
