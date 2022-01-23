from ast_class_definitions import *

# binop, number, bool, new id, null, invocation, unary, dot, id
# returns (resultRegNum, llvm code)
# function_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
def expressionToLLVM(lastRegUsed:int, expression, function_env) -> Tuple[int, list[str]]:
    match expression:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expression, function_env)
        case m_num() | m_bool():
            return lastRegUsed, expression.val
        case m_new_struct():
            pass
        case m_null():
            pass
        case m_invocation():
            return invocationToLLVM(lastRegUsed, expression, function_env)
        case m_unary():
            return unaryToLLVM(lastRegUsed, expression, function_env) 
        case m_dot():
            pass
        case m_id():
            return lastRegUsed+1, [f'%tmp{lastRegUsed+1} = load i64* %{expression.identifier}']


def invocationToLLVM(lastRegUsed:int, exp:m_invocation, function_env: dict) -> Tuple[int, list[str]]:

    params = []
    for i in range(len(exp.args_expressions)):
        params.append(expressionToLLVM(lastRegUsed, exp.args_expressions[i], function_env))
        lastRegUsed = params[-1][0]

    targetReg = params[-1][0] + 1
    returnTypeFunID = None
    parameters = []

    formatString = '%%tmp%s = call %s(%s)'

    match function_env[exp.id.identifier][0].typeID:
        case 'int' | 'bool':
            returnTypeFunID = f'i64 @{exp.id.identifier}'
        case typeID:
            returnTypeFunID = f'%struct.{typeID} @{exp.id}'

    for i in range(len(params)):
        paramReg = params[i][0]
        paramCode = params[i][1]
        match paramCode:
            case True | False:
                parameters.append(f'i64 {int(paramCode)}')
            case int():
                parameters.append(f'i64 {paramCode}')
            case other:
                paramType = function_env[exp.id.identifier][1][i].typeID
                parameters.append(f'%struct.{paramType} %tmp{paramReg}')
    
    parameters = ', '.join(parameters)

    instructions = []
    for paramReg, code in params:
        if type(code) == list:
            instructions.append(code)
    instructions.append(formatString%(targetReg, returnTypeFunID, parameters))

    return (targetReg, instructions)


# ! -
def unaryToLLVM(lastRegUsed:int, exp:m_unary, function_env) -> Tuple[int, list[str]]:
    operandReg, operandCode = expressionToLLVM(lastRegUsed, exp.operand_expression, function_env)

    s1 = operandReg + 1
    s2 = None
    s3 = None

    formatString = '%%tmp%s = %s, %s'

    match operandCode:
        case True | False:
            s3 = int(operandCode)
        case int():
            s3 = operandCode
        case other:
            s3 = f'%tmp{operandReg}'

    match exp.operator:
        case '!':
            s2 = f'xor i64 1'
        case '-':
            s2 = f'mul i64 -1'

    if type(operandCode) == list: 
        operandCode.append(formatString%(s1, s2, s3))
    else:
        operandCode = [formatString%(s1, s2, s3)]
    return (s1, operandCode)


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, exp:m_binop, function_env):
    leftOpReg, leftOpCode = expressionToLLVM(lastRegUsed, exp.left_expression, function_env)
    rightOpReg, rightOpCode = expressionToLLVM(leftOpReg, exp.right_expression, function_env)

    targetReg = rightOpReg + 1
    instrAndDatatype = None
    leftOperand = None
    rightOperand = None

    formatString = '%%tmp%s = %s %s, %s'

    match leftOpCode:
        case True | False:
            leftOperand = int(leftOpCode)
        case int():
            leftOperand = leftOpCode
        case other:
            leftOperand = f'%tmp{leftOpReg}'

    match rightOpCode:
        case True | False:
            rightOperand = int(rightOpCode)
        case int():
            rightOperand = rightOpCode
        case other:
            rightOperand = f'%tmp{rightOpReg}'

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

    return (rightOpReg+1, instructions)