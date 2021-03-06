from ast_class_definitions import *

# env structure : {str: m_type}
# f_env structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types
# t_env structure: {str: list[m_declaration]}


def toLLVM(ast:m_prog):
    output = []

    # add the llvm code to define struct types
    for typeDecl in ast.types:
        output.append(typeDecl.getLLVM())

    type_sizes = ast.getTypeSizes()
    lastRegUsed = 0
    # add llvm code to define global variables
    for varDecl in ast.global_declarations:
        output.extend(varDecl.getSSAGlobals())
        # if declaration is a struct, will use one register in its declaration
        if varDecl.type.typeID != 'int' and varDecl.type.typeID != 'bool' and varDecl.type.typeID != 'null':
            lastRegUsed += 1

    top_env = ast.getTopEnv()
    type_env = ast.getTypes()
    
    fun_env = {}
    for function in ast.functions:
        lastRegUsed, fun_env, funCode = functionToLLVM(lastRegUsed, function, top_env, type_env, fun_env, type_sizes)
        output.extend(funCode)

    return output


def functionToLLVM(lastRegUsed, func:m_function, top_env, type_env, fun_env, type_sizes):
    code = []
    
    params = []
    paramTypes = []
    for param in func.param_declarations:
        paramTypes.append(param.type)
        params.append(f'{getLLVMType(param.type.typeID)} %{param.id.identifier}')
        top_env[param.id.identifier] = param.type
    params = ', '.join(params)
    
    code.append(f'define {getLLVMType(func.return_type.typeID)} @{func.id.identifier}({params})' + ' {')
    if func.id.identifier == 'main':
        code.append('entry:')

    for declaration in func.body_declarations:
        top_env[declaration.id.identifier] = declaration.type
        code.append(declaration.getSSALocals())

    lastRegUsed = 0
    for statement in func.statements:
        stmtReg, stmtType, stmtCode = statementToLLVM(lastRegUsed, statement, top_env, type_env, fun_env)
        lastRegUsed = stmtReg
        code.extend(stmtCode)

    code.append('}')

    fun_env[func.id.identifier] = (func.return_type, paramTypes)

    return lastRegUsed, fun_env, code



# define i32 @mul_add(i32 %x, i32 %y, i32 %z) {
# entry:
#   %tmp = mul i32 %x, %y
#   %tmp2 = add i32 %tmp, %z
#   ret i32 %tmp2
# }

# statements = assignment | print | conditional | loop | delete | ret | invocation
# returns (last register used, llvm type in last reg used, llvm instruction list)
def statementToLLVM(lastRegUsed: int, stmt, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    match stmt:
        case m_assignment():
            return assignToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_print():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, env, t_env, f_env)
            if type(exprCode) == list:
                instruction = f'%t{exprReg + 1} = call i32 @printf("%d", %t{exprReg})'
                exprCode.append(instruction)
                return exprReg + 1, 'i32', exprCode
            else:
                instruction = f'%t{exprReg + 1} = call i32 @printf("%d", {exprCode})'
                return exprReg + 1, 'i32', [instruction]
        case m_delete():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, env, t_env, f_env)
            exprCode.extend([f'%t{exprReg + 1} = bitcast {exprType} %t{exprReg} to i8*',
                            f'call void @free(%{exprReg + 1})'])
            return exprReg + 1, 'void', exprCode
        case m_conditional():
            return condToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_loop():
            return loopToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_ret():
            return retToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_invocation():
            return invocationToLLVM(lastRegUsed, stmt, env, t_env, f_env)


def loopToLLVM(lastRegUsed:int, loop:m_loop, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    code = []
    guardReg, guardType, guardCode = expressionToLLVM(lastRegUsed, loop.guard_expression, env, t_env, f_env)

    if type(guardCode) == list:
        code.append(f'l{guardReg+1}:')
        code.extend(guardCode)
        code.append(f'br i1 %t{guardReg}, label %l{guardReg+2}, label %l{guardReg+3}')
    else:
        code = [f'l{guardReg+1}:',f'br i1 {guardCode}, label %l{guardReg+2}, label %l{guardReg+3}']

    lastRegUsed = guardReg+3

    whileBlockCode = [f'l{guardReg + 2}:']
    for statement in loop.body_statements:
        t1, t2, t3 = statementToLLVM(lastRegUsed, statement, env, t_env, f_env)
        whileBlockCode.extend(t3)
        lastRegUsed = t1
    whileBlockCode.append(f'br label %l{guardReg + 1}')
    whileBlockCode.append(f'l{guardReg+3}:')
    code.extend(whileBlockCode)
    return (lastRegUsed, t2, code)



def condToLLVM(lastRegUsed:int, stmt:m_conditional, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    guardReg, guardType, guardCode = expressionToLLVM(lastRegUsed, stmt.guard_expression, env, t_env, f_env)

    if type(guardCode) == list:
        guardCode.append(f'br i1 %t{guardReg}, label %l{guardReg+1}, label %l{guardReg+2}')
    else:
        guardCode = [f'br i1 {guardCode}, label %l{guardReg+1}, label %l{guardReg+2}']

    lastRegUsed = guardReg + 3

    ifCode = [f'l{guardReg + 1}:']
    for statement in stmt.if_statements:
        t1, t2, t3 = statementToLLVM(lastRegUsed, statement, env, t_env, f_env)
        ifCode.extend(t3)
        lastRegUsed = t1
    ifCode.append(f'br label %l{guardReg+3}')
    thenCode = []

    if stmt.else_statements[0] != None:
        thenCode = [f'l{guardReg + 2}:']
        for statement in stmt.else_statements:
            t1, t2, t3 = statementToLLVM(lastRegUsed, statement, env, t_env, f_env)
            thenCode.extend(t3)
            lastRegUsed = t1
        thenCode.append(f'br label %l{guardReg+3}')
        
    guardCode.extend(ifCode)
    guardCode.extend(thenCode)
    guardCode.append(f'l{guardReg+3}:')
    return (lastRegUsed, t2, guardCode)


def assignToLLVM(lastRegUsed:int, assign:m_assignment, env, t_env, f_env) -> Tuple[int, str, list[str]]:

    exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, assign.source_expression, env, t_env, f_env)
    lastRegUsed = exprReg

    if type(exprCode) == list:
        outputCode = exprCode
        immediateVal = False
    else:
        outputCode = []
        immediateVal = True

    currentID = assign.target_ids[0].identifier
    currentIDTypeID = env[currentID].typeID
    
    nested = False
    for accessedm_id in assign.target_ids[1:]:
        nested = True
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, t_env[currentIDTypeID])

        if type(currentID) == int:
            instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %t{currentID}, i32 0, i32 {accessedIDmemNum}'
        else:
            instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    if type(currentID) == int:
        currentID = f't{currentID}'

    if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
        if immediateVal:
            outputCode.append(f'store i32 {exprCode}, i32* %{currentID}')
            return lastRegUsed, 'i32', outputCode
        else:
            outputCode.append(f'store i32 %t{exprReg}, i32* %{currentID}')
            return lastRegUsed, 'i32', outputCode
    #(f'store %struct.s1* %1, %struct.s1** %2')
    else:
        llvmType = getLLVMType(currentIDTypeID)
        if nested:
            outputCode.append(f'store {llvmType} %t{exprReg}, {llvmType}* %{currentID}')
            return lastRegUsed, llvmType, outputCode
        else:
            outputCode.append(f'%{currentID} = add {llvmType} %t{exprReg}, 0')
            return lastRegUsed, getLLVMType(currentIDTypeID), outputCode

    
    # elif exprType != 'i32':
    #     exprType = f'%struct.{exprType}'
    
    # store i32 3, i32* %2, align 4  WHERE 3 is value to store, %2 holds address of target


def retToLLVM(lastRegUsed, ret:m_ret, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    returnReg, retType, returnCode = expressionToLLVM(lastRegUsed, ret.expression, env, t_env, f_env)

    if type(returnCode) == list:
        returnCode.append(f'ret {retType} %t{returnReg}')
        return (returnReg, retType, returnCode)
    elif returnCode == 'void':
        return (returnReg, retType, [f'ret {retType}'])
    else:
        return (returnReg, retType, [f'ret {retType} {returnCode}'])


def getLLVMType(typeID:str) -> str:
    if typeID == 'bool' or typeID == 'int':
        return 'i32'
    elif typeID == 'void':
        return 'void'
    else:
        return f'%struct.{typeID}*'


# expressions = binop, number, bool, new id, null, invocation, unary, dot, id
# returns (return register, llvm return type, llvm instruction list)
def expressionToLLVM(lastRegUsed:int, expression, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    match expression:
        case None:
            return lastRegUsed, 'void', 'void'
        case m_binop():
            return binaryToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_num():
            return lastRegUsed, 'i32', int(expression.val)
        case m_bool():
            return lastRegUsed, 'i1', int(expression.val)
        case m_new_struct():
            code = [f'%t{lastRegUsed + 1} = call i8* @malloc({len(t_env[expression.struct_id.identifier]) * 4})',
                 f'%t{lastRegUsed + 1} = bitcast i8* %t{lastRegUsed + 1} to %struct.{expression.struct_id.identifier}*']
            return lastRegUsed+1, f'%struct.{expression.struct_id.identifier}*', code
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return lastRegUsed, 'i32', 0
        case m_invocation():
            return invocationToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_read():
            return lastRegUsed+2, 'i32', [f'%t{lastRegUsed+2} = alloc i32', f'%t{lastRegUsed+1} = call i32 @scanf("%d", %t{lastRegUsed+2}*)']
        case m_unary():
            return unaryToLLVM(lastRegUsed, expression, env, t_env, f_env) 
        case m_dot():
            return dotToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_id():
            idType = env[expression.identifier]
            if idType == m_type('bool') or idType == m_type('int'):
                return lastRegUsed+1, 'i32', [f'%t{lastRegUsed+1} = load i32, i32* %{expression.identifier}']
            else:
                llvmType = getLLVMType(idType.typeID)
                return lastRegUsed+1, llvmType, [f'%t{lastRegUsed+1} = add {llvmType} %{expression.identifier}, 0']


def dotToLLVM(lastRegUsed:int, expression:m_dot, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = env[currentID].typeID

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, t_env[currentIDTypeID])

        if type(currentID) == int:
            currentID = f't{currentID}'
        instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    if type(currentID) == int:
        currentID = f't{currentID}'
    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i32 or %struct.__*
    outputCode.append(f'%t{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)



def invocationToLLVM(lastRegUsed:int, exp:m_invocation, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    params = []
    for expression in exp.args_expressions:
        params.append(expressionToLLVM(lastRegUsed, expression, env, t_env, f_env))
        lastRegUsed = params[-1][0]

    targetReg = params[-1][0] + 1
    returnTypeID = getLLVMType(f_env[exp.id.identifier][0].typeID)
    funID = exp.id.identifier

    parameters = []
    instructions = []

    for paramReg, paramType, paramCode in params:
        if type(paramCode) == list:
            parameters.append(f'{paramType} %t{paramReg}')
            instructions.extend(paramCode)
        else:
            parameters.append(f'i32 {paramCode}')
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    instructions.append(f'%t{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return (targetReg, returnTypeID, instructions)


# ! -
def unaryToLLVM(lastRegUsed:int, exp:m_unary, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    operandReg, operandType, operandCode = expressionToLLVM(lastRegUsed, exp.operand_expression, env, t_env, f_env)

    match exp.operator:
        case '!':
            op = f'xor i1 1'
        case '-':
            op = f'mul i32 -1'
        
    if type(operandCode) == list:
        operandCode.append(f'%t{operandReg + 1} = {op}, %t{operandReg}')
        return (operandReg+1, 'i32', operandCode)
    else:
        return (operandReg+1, 'i32', [f'%t{operandReg + 1} = {op}, {operandCode}'])


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, exp:m_binop, env, t_env, f_env):
    leftOpReg, leftLLVMType, leftOpCode = expressionToLLVM(lastRegUsed, exp.left_expression, env, t_env, f_env)
    rightOpReg, rightLLVMType, rightOpCode = expressionToLLVM(leftOpReg, exp.right_expression, env, t_env, f_env)

    # == != <= < > >= - + * / || &&
    match exp.operator:
        case '==':
            op = 'icmp eq i1'
        case '!=':
            op = 'icmp ne i1'
        case '<=':
            op = 'icmp sle i1'
        case '<':
            op = 'icmp slt i1'
        case '>=':
            op = 'icmp sge i1'
        case '>':
            op = 'icmp sgt i1'
        case '-':
            op = 'sub i32'
        case '+':
            op = 'add i32'
        case '*':
            op = 'mul i32'
        case '/':
            op = 'div i32'
        case '||':
            op = 'or i1'
        case '&&':
            op = 'and i1'

    instructions = []
    targetReg = rightOpReg + 1
    if type(leftOpCode) == list:
        instructions.extend(leftOpCode)
        leftOpReg = '%t' + str(leftOpReg)
    else:
        leftOpReg = leftOpCode
    
    if type(rightOpCode) == list:
        instructions.extend(rightOpCode)
        rightOpReg = '%t' + str(rightOpReg)
    else:
        rightOpReg = rightOpCode


    instructions.append(f'%t{targetReg} = {op} {leftOpReg}, {rightOpReg}')

    return (targetReg , 'i32', instructions)

# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)
