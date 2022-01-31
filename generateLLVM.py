from cmath import exp
from ast_class_definitions import *

# env structure : {str: m_type}
# f_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
# t_env structure: {str: list[m_declaration]}

# statements = assignment | print | conditional | loop | delete | ret | invocation
# returns (last register used, llvm instruction list)
def statementToLLVM(lastRegUsed: int, stmt, env, t_env, f_env) -> Tuple[int, list[str]]:
    match stmt:
        case m_assignment():
            return assignToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_print():
            pass
        case m_conditional():
            return condToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_loop():
            pass
        case m_delete():
            pass
        case m_ret():
            return retToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_invocation():
            return invocationToLLVM(lastRegUsed, stmt, env, t_env, f_env)


def condToLLVM(lastRegUsed:int, stmt:m_conditional, env, t_env, f_env):
    guardReg, guardType, guardCode = expressionToLLVM(lastRegUsed, stmt.guard_expression, env, t_env, f_env)

    guardCode.append(f'br i1 %{guardReg}, label %{guardReg+1}, label {guardReg+2}')
    ifBlock = f''
    thenBlock = f''
    finalBlock = f''


def assignToLLVM(lastRegUsed:int, assign:m_assignment, env, t_env, f_env):

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
    
    for accessedm_id in assign.target_ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, t_env[currentIDTypeID])

        instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1
    


    if immediateVal:
        instruction = f'store i64 {exprCode}, i64* %{currentID}'
        outputCode.append(instruction)
        return (lastRegUsed, 'i64*', outputCode)
    else:
        if currentIDTypeID == 'int' or currentIDTypeID == 'bool':
            currentIDTypeID = getLLVMType(currentIDTypeID)
            instruction = f'store {exprType} %{exprReg}, {currentIDTypeID}* %{lastRegUsed}'
            outputCode.append(instruction)
            return (lastRegUsed, f'{currentIDTypeID}*', outputCode)
        else:
            instruction = f'store {exprType} %{exprReg}, %struct.{currentIDTypeID}** %{currentID}'
            outputCode.append(instruction)
            return (lastRegUsed, f'%struct.{currentIDTypeID}*', outputCode)

    
    # elif exprType != 'i64':
    #     exprType = f'%struct.{exprType}'
    
    # store i32 3, i32* %2, align 4  WHERE 3 is value to store, %2 holds address of target

def retToLLVM(lastRegUsed, ret:m_ret, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    returnReg, retType, returnCode = expressionToLLVM(lastRegUsed, ret.expression, env, t_env, f_env)

    if type(returnCode) == list:
        returnCode.append(f'ret {retType} %{returnReg}')
        return (returnReg, retType, returnCode)
    else:
        return (returnReg, retType, [f'ret {retType} {returnCode}'])

def getLLVMType(typeID:str) -> str:
    if typeID == 'bool' or typeID == 'int':
        return 'i64'
    else:
        return f'%struct.{typeID}*'

# expressions = binop, number, bool, new id, null, invocation, unary, dot, id
# returns (return register, llvm return type, llvm instruction list)
def expressionToLLVM(lastRegUsed:int, expression, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    match expression:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_num() | m_bool():
            return lastRegUsed, 'i64', int(expression.val)
        case m_new_struct():
            return lastRegUsed+1, f'%struct.{expression.struct_id.identifier}*', [f'%{lastRegUsed + 1}=alloca %struct.{expression.struct_id.identifier}']
        case m_null():
            raise NotImplementedError()
        case m_invocation():
            return invocationToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_read():
            pass
        case m_unary():
            return unaryToLLVM(lastRegUsed, expression, env, t_env, f_env) 
        case m_dot():
            return dotToLLVM(lastRegUsed, expression, env, t_env, f_env)
        case m_id():
            idType = env[expression.identifier]
            if idType == m_type('bool') or idType == m_type('int'):
                return lastRegUsed+1, 'i64', [f'%{lastRegUsed+1} = load i64, i64* %{expression.identifier}']
            else:
                return lastRegUsed+1, f'%struct.{idType.typeID}*', [f'%{lastRegUsed+1} = load %struct.{idType.typeID}*, %struct.{idType.typeID}** %{expression.identifier}']


def dotToLLVM(lastRegUsed:int, expression:m_dot, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = env[currentID].typeID

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, t_env[currentIDTypeID])

        instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i64 or %struct.__*
    outputCode.append(f'%{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)


# returns (struct member num, member typeID)
def getNestedDeclaration(id:str, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)


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
            parameters.append(f'{paramType} %{paramReg}')
            instructions.extend(paramCode)
        else:
            parameters.append(f'i64 {paramCode}')
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    instructions.append(f'%{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return (targetReg, returnTypeID, instructions)


# ! -
def unaryToLLVM(lastRegUsed:int, exp:m_unary, env, t_env, f_env) -> Tuple[int, str, list[str]]:
    operandReg, operandType, operandCode = expressionToLLVM(lastRegUsed, exp.operand_expression, env, t_env, f_env)

    match exp.operator:
        case '!':
            op = f'xor i64 1'
        case '-':
            op = f'mul i64 -1'
        
    if type(operandCode) == list:
        operandCode.append(f'%{operandReg + 1} = {op}, %{operandReg}')
        return (operandReg+1, 'i64', operandCode)
    else:
        return (operandReg+1, 'i64', [f'%{operandReg + 1} = {op}, {operandCode}'])


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, exp:m_binop, env, t_env, f_env):
    leftOpReg, leftLLVMType, leftOpCode = expressionToLLVM(lastRegUsed, exp.left_expression, env, t_env, f_env)
    rightOpReg, rightLLVMType, rightOpCode = expressionToLLVM(leftOpReg, exp.right_expression, env, t_env, f_env)

    # == != <= < > >= - + * / || &&
    match exp.operator:
        case '==':
            op = 'icmp eq i64'
        case '!=':
            op = 'icmp ne i64'
        case '<=':
            op = 'icmp sle i64'
        case '<':
            op = 'icmp slt i64'
        case '>=':
            op = 'icmp sge i64'
        case '>':
            op = 'icmp sgt i64'
        case '-':
            op = 'sub i64'
        case '+':
            op = 'add i64'
        case '*':
            op = 'mul i64'
        case '/':
            op = 'div i64'
        case '||':
            op = 'or i64'
        case '&&':
            op = 'or i64'

    instructions = []
    targetReg = rightOpReg + 1
    if type(leftOpCode) == list:
        instructions.extend(leftOpCode)
        leftOpReg = '%' + str(leftOpReg)
    else:
        leftOpReg = leftOpCode
    
    if type(rightOpCode) == list:
        instructions.extend(rightOpCode)
        rightOpReg = '%' + str(rightOpReg)
    else:
        rightOpReg = rightOpCode


    instructions.append(f'%{targetReg} = {op} {leftOpReg}, {rightOpReg}')

    return (targetReg , 'i64', instructions)