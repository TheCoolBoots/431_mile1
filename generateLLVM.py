from ast_class_definitions import *

# env structure : {str: m_type}
# f_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
# t_env structure: {str: list[m_declaration]}

# statements = assignment | print | conditional | loop | delete | ret | invocation
# returns (last register used, llvm instruction list)
def statementToLLVM(lastRegUsed: int, stmt, env, t_env, f_env) -> Tuple[int, list[str]]:
    match stmt:
        case m_assignment():
            pass
        case m_print():
            pass
        case m_conditional():
            pass
        case m_loop():
            pass
        case m_delete():
            pass
        case m_ret():
            return retToLLVM(lastRegUsed, stmt, env, t_env, f_env)
        case m_invocation():
            return invocationToLLVM(lastRegUsed, stmt, env, f_env, t_env)


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
            return binaryToLLVM(lastRegUsed, expression, env, f_env, t_env)
        case m_num() | m_bool():
            return lastRegUsed, 'i64', expression.val
        case m_new_struct():
            return lastRegUsed+1, f'%struct.{expression.struct_id.identifier}*', [f'%{lastRegUsed + 1}=alloca %struct.{expression.struct_id.identifier}']
        case m_null():
            raise NotImplementedError()
        case m_invocation():
            return invocationToLLVM(lastRegUsed, expression, env, f_env, t_env)
        case m_read():
            pass
        case m_unary():
            return unaryToLLVM(lastRegUsed, expression, env, f_env, t_env) 
        case m_dot():
            return dotToLLVM(lastRegUsed, expression, env, f_env, t_env)
        case m_id():
            idType = env[expression.identifier]
            if idType == m_type('bool') or idType == m_type('int'):
                return lastRegUsed+1, 'i64', [f'%{lastRegUsed+1} = load i64 %{expression.identifier}']
            else:
                return lastRegUsed+1, f'%struct.{idType.typeID}*', [f'%{lastRegUsed+1} = load %struct.{idType.typeID}* %{expression.identifier}']

def dotToLLVM(lastRegUsed:int, expression:m_dot, env, f_env, t_env) -> Tuple[int, str, list[str]]:
    rootType = env[expression.ids[0].identifier].typeID
    
    formatString = '%%%s = getelementptr %s, %s %%%s, i32 0, i32 %s'
    sourceID = expression.ids[0].identifier

    code = []

    # first id will map to an instance of a struct
    # other ids may or may not map to struct
    for id in expression.ids[1:]:

        # t_env[rootType] will return a list of m_declarations
        # getNestedDeclaration will check if the id exists within the root type
        # struct A {
        #   int a
        # };
        # struct A instance
        # int tmp = instance.a      need to know what the type of a is so load works correctly
        structIndex, outputTypeID = getNestedDeclaration(id, t_env[rootType])
        targetRegister = lastRegUsed + 1
        sourceType = f'%struct.{rootType}'

        code.append(formatString%(targetRegister, sourceType, f'{sourceType}*', sourceID, structIndex))
        
        lastRegUsed += 1
        sourceID = targetRegister
        rootType = outputTypeID

    if outputTypeID == 'int' or outputTypeID == 'bool':
        code.append(f'%{lastRegUsed + 1} = load i64, i64* %{targetRegister}')
    else:
        code.append(f'%{lastRegUsed + 1} = load {outputTypeID}*, {outputTypeID}* %{targetRegister}')



    return (lastRegUsed + 1, getLLVMType(outputTypeID), code)

# returns (struct member num, member typeID)
def getNestedDeclaration(id:str, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)

def invocationToLLVM(lastRegUsed:int, exp:m_invocation, env, f_env, t_env) -> Tuple[int, str, list[str]]:

    params = []
    for i in range(len(exp.args_expressions)):
        params.append(expressionToLLVM(lastRegUsed, exp.args_expressions[i], env, f_env, t_env))
        lastRegUsed = params[-1][0]

    targetReg = params[-1][0] + 1
    returnTypeID = None
    funID = None
    parameters = []

    formatString = '%%%s = call %s %s(%s)'

    # get return type of function
    match f_env[exp.id.identifier][0].typeID:
        case 'int' | 'bool':
            returnTypeID = f'i64'
            funID = f'@{exp.id.identifier}'
        case typeID:
            # need to write a test case for this part
            returnTypeID = f'%struct.{typeID}*'
            funID = f'@{exp.id}'

    # get the paramater types & registers where they are being stored
    for i in range(len(params)):
        paramReg = params[i][0]
        paramCode = params[i][2]
        match paramCode:
            case True | False:
                parameters.append(f'i64 {int(paramCode)}')
            case int():
                parameters.append(f'i64 {paramCode}')
            case other:
                # need to write a test case for this part
                paramType = f_env[exp.id.identifier][1][i].typeID
                parameters.append(f'%struct.{paramType}* %{paramReg}')
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)

    instructions = []
    for paramReg, retType, code in params:
        if type(code) == list:
            instructions.extend(code)
    instructions.append(formatString%(targetReg, returnTypeID, funID, parameters))

    return (targetReg, returnTypeID, instructions)


# ! -
def unaryToLLVM(lastRegUsed:int, exp:m_unary, env, f_env, t_env) -> Tuple[int, str, list[str]]:
    operandReg, operandType, operandCode = expressionToLLVM(lastRegUsed, exp.operand_expression, env, f_env, t_env)

    s1 = operandReg + 1
    s2 = None
    s3 = None

    formatString = '%%%s = %s, %s'

    match operandCode:
        case True | False:
            s3 = int(operandCode)
        case int():
            s3 = operandCode
        case other:
            s3 = f'%{operandReg}'

    match exp.operator:
        case '!':
            s2 = f'xor i64 1'
        case '-':
            s2 = f'mul i64 -1'

    if type(operandCode) == list: 
        operandCode.append(formatString%(s1, s2, s3))
    else:
        operandCode = [formatString%(s1, s2, s3)]
    return (s1, 'i64', operandCode)


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, exp:m_binop, env, f_env, t_env):
    leftOpReg, leftLLVMType, leftOpCode = expressionToLLVM(lastRegUsed, exp.left_expression, env, f_env, t_env)
    rightOpReg, leftLLVMType, rightOpCode = expressionToLLVM(leftOpReg, exp.right_expression, env, f_env, t_env)

    targetReg = rightOpReg + 1
    instrAndDatatype = None
    leftOperand = None
    rightOperand = None

    formatString = '%%%s = %s %s, %s'

    match leftOpCode:
        case True | False:
            leftOperand = int(leftOpCode)
        case int():
            leftOperand = leftOpCode
        case other:
            leftOperand = f'%{leftOpReg}'

    match rightOpCode:
        case True | False:
            rightOperand = int(rightOpCode)
        case int():
            rightOperand = rightOpCode
        case other:
            rightOperand = f'%{rightOpReg}'

    # == != <= < > >= - + * / || &&
    match exp.operator:
        case '==':
            instrAndDatatype = 'icmp eq i64'
        case '!=':
            instrAndDatatype = 'icmp ne i64'
        case '<=':
            instrAndDatatype = 'icmp sle i64'
        case '<':
            instrAndDatatype = 'icmp slt i64'
        case '>=':
            instrAndDatatype = 'icmp sge i64'
        case '>':
            instrAndDatatype = 'icmp sgt i64'
        case '-':
            instrAndDatatype = 'sub i64'
        case '+':
            instrAndDatatype = 'add i64'
        case '*':
            instrAndDatatype = 'mul i64'
        case '/':
            instrAndDatatype = 'div i64'
        case '||':
            instrAndDatatype = 'or i64'
        case '&&':
            instrAndDatatype = 'or i64'

    instructions = leftOpCode
    if type(instructions) is list:
        if type(rightOpCode) is list:
            instructions.extend(rightOpCode)
    else:
        if type(rightOpCode) is list:
            instructions = rightOpCode
        else:
            instructions = []

    instructions.append(formatString%(targetReg, instrAndDatatype, leftOperand,rightOperand))

    return (targetReg, 'i64', instructions)