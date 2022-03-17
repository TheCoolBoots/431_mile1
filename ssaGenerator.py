from typing import Tuple
from ast_class_definitions import *
from cfg_generator import CFG_Node
from generateLLVM import getLLVMType


# top_env structure: {str: (bool, m_type)}              where bool == true if global, false if local 
# types structure: {str: list[m_declaration]}
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# functions structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types
# {str funName: (m_type returnType, list[m_type] paramTypes)}


# returns int: lastRegUsed, list[str]: llvm code for statements within currentNode, dict: ssa mappings
def generateSSA(lastRegUsed, currentNode: CFG_Node, top_env:dict, types:dict, functions:dict) -> Tuple[int, list[str]]:
    code = []

    for statement in currentNode.ast_statements:
        lastRegUsed, llvmType, newCode = statementToSSA(lastRegUsed, statement, top_env, types, functions, currentNode)
        code.extend(newCode)

    return lastRegUsed, code


# env maps strings to types {str: bool, str(typeID)}
# r_ = load type[id] @z
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# returns a tuple containing (mappings within block, SSA LLVM code)
def statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case m_print():
            exprReg, exprType, exprCode = expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            
            if 'immediate' not in exprType:
                lastRegUsed = exprReg
                exprReg = f'%t{exprReg}'
            else:
                exprType = exprType.split('_')[0]
            
            instruction = f'%t{lastRegUsed + 1} = call i32 @printf("%d", {exprReg})'
            exprCode.append(instruction)
            return lastRegUsed + 1, 'i32', exprCode
        case m_delete():
            exprReg, exprType, exprCode = expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            
            if 'immediate' not in exprType:
                lastRegUsed = exprReg
                # exprReg = f'%t{exprReg}'
            else:
                exprType = exprType.split('_')[0]
            
            if type(exprReg) != str:
                lastRegUsed = exprReg
            exprCode.extend([f'%t{lastRegUsed + 1} = bitcast {exprType} %t{exprReg} to i8*',
                            f'call void @free(%t{lastRegUsed + 1})'])
            # env.pop(exprReg)
            return lastRegUsed + 1, 'void', exprCode
        case m_ret():
            return retToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized structure:{other}')
            return lastRegUsed, -1, -1


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        return (lastRegUsed, 'void', [f'%t0 = void', f'br label %retLabel'])

    returnReg, retType, returnCode = expressionToSSA(lastRegUsed, ret.expression, env, types, functions, currentNode)

    if 'immediate' not in retType:
        returnReg = f'%t{returnReg}'
    else:
        retType = retType.split('_')[0]

    if(retType == 'void'):
        returnCode.append(f'%t0 = void')
    else:
        returnCode.append(f'%t0 = add {retType} {returnReg}, 0')
    returnCode.append(f'br label %retLabel')

    return (returnReg, retType, returnCode)


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    exprReg, exprType, exprCode = expressionToSSA(lastRegUsed, assign.source_expression, env, types, functions, currentNode)

    if 'immediate' not in exprType:
        lastRegUsed = exprReg
        exprReg = f'%t{exprReg}'
        immediate = False
    else:
        exprType = exprType.split('_')[0]
        immediate = True

    targetStrings = [mid.identifier for mid in assign.target_ids]

    if len(targetStrings) == 1:
        # if the target is in the top_env, that means it is either a global var or global/local struct
        #       if global var, use @
        #       if local struct, use normal
        if targetStrings[0] in env:
            if env[targetStrings[0]] == m_type('int') or env[targetStrings[0]] == m_type('bool'):
                exprCode.append(f'store {exprType} {exprReg}, i32* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # if struct is a global struct
            elif env[targetStrings[0]][0]:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} {exprReg}, {typeStr}* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # struct is a locally defined struct
            else:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} {exprReg}, {typeStr}* %{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode

        # if it is not in top_env, it is a local variable and is dealt with through SSA form

        if immediate:
            exprType = exprType + '_immediate'
        if type(exprReg) == str:
            exprReg = int(exprReg[2:])
        currentNode.mappings[targetStrings[0]] = (exprType, exprReg, currentNode.id)
        return lastRegUsed, exprType, exprCode
    else:   # target expression is a struct (A.a.b)
        currentID = assign.target_ids[0].identifier
        currentIDTypeID = env[currentID][1].typeID
        
        nested = False
        for accessedm_id in assign.target_ids[1:]:
            nested = True
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

            if currentID in env and env[currentID][0]:
                instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
            else:
                instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
            exprCode.append(instruction)

            currentID = lastRegUsed + 1
            currentIDTypeID = accessedTypeID
            lastRegUsed += 1

        # if type(exprReg) == int:
        #     exprReg = f'%t{exprReg}'

        if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
            exprCode.append(f'store i32 {exprReg}, i32* %t{currentID}')
            return lastRegUsed, 'i32', exprCode
        #(f'store %struct.s1* %1, %struct.s1** %2')
        else:
            if nested:
                llvmType = getLLVMType(currentIDTypeID)
                exprCode.append(f'store {llvmType} {exprReg}, {llvmType}* %t{currentID}')
                return lastRegUsed, llvmType, exprCode
            else:
                # TODO can't assign registers to registers in llvm
                exprCode.append(f'%t{currentID} = add i32 {exprReg}, 0')
                return lastRegUsed, getLLVMType(currentIDTypeID), exprCode
    

# returns a tuple containing (resultReg, llvmType, SSA LLVM code)
def expressionToSSA(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, env, types, functions, currentNode)
        case m_num():
            return expr.val, 'i32_immediate', []
        case m_bool():
            return int(expr.val), 'i1_immediate', []
        case m_new_struct():
            code = [f'%t{lastRegUsed + 1} = call i8* @malloc({len(types[expr.struct_id.identifier]) * 4})',
                 f'%t{lastRegUsed + 1} = bitcast i8* %t{lastRegUsed + 1} to %struct.{expr.struct_id.identifier}*']
            return lastRegUsed+1, f'%struct.{expr.struct_id.identifier}*', code
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return lastRegUsed+1, 'i32', [f'%t{lastRegUsed+1} = add i32 0, 0']
        case m_invocation():
            return invocationToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_read():
            return lastRegUsed+2, 'i32', [f'%t{lastRegUsed+2} = alloc i32', f'%t{lastRegUsed+1} = call i32 @scanf("%d", %t{lastRegUsed+2}*)']
        case m_unary():
            return unaryToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_dot():
            return dotToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_id():
            if expr.identifier in env:
                # if id is a global variable
                if env[expr.identifier][0]:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%t{lastRegUsed+1} = load {llvmType}* @{expr.identifier}']
                # id is a local struct
                else:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%t{lastRegUsed+1} = load {llvmType}* %{expr.identifier}']
            # handle with SSA form
            exprReg, llvmType, code, lastLabel = readVariable(lastRegUsed, expr.identifier, currentNode, currentNode)
            return exprReg, llvmType, code
        case other:
            print(f'ERROR: unrecognized expression: {other}')


# mappings structure = {str id: (str llvmType, int regNum, int prevBlock)}
# returns lastRegUsed, llvmType, code, preceeding label
def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node, sourceNode:CFG_Node) -> Tuple[int, str, list[str], int]:
    if identifier in currentNode.mappings:
        if 'immediate' in currentNode.mappings[identifier][0]:
            return currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], [], currentNode.mappings[identifier][2]
        else:
            return f'%t{currentNode.mappings[identifier][1]}', f'{currentNode.mappings[identifier][0]}_immediate', [], currentNode.mappings[identifier][2]
    else:
        if not currentNode.sealed:
            # guard block isnt sealed yet, therefore it goes into this one
            # structs will never go into mappings so hard coding i32 is fine here
            # sourceNode.sealed = False
            if type(lastRegUsed) != int:
                lastRegUsed = int(lastRegUsed[2:])
            sourceNode.mappings[identifier] = ('i32', lastRegUsed+1, sourceNode.id)
            return lastRegUsed+1, 'i32', [f'{lastRegUsed+1}-{sourceNode.id}-{identifier}-*'], sourceNode.id
        elif len(currentNode.prevNodes) == 0:
            # val is undefined
            # should never encounter this case
            pass
        elif len(currentNode.prevNodes) == 1:
            # call expressionToLLVM with expr and prev block's mappings
            prevNode = currentNode.prevNodes[0]
            return readVariable(lastRegUsed, identifier, prevNode, currentNode)
        else:
            # create phi node with values in prev blocks
            possibleRegisters = [readVariable(lastRegUsed, identifier, node, sourceNode) for node in currentNode.prevNodes]
            llvmType = possibleRegisters[0][1]
            if 'immediate' in llvmType:
                llvmType = llvmType.replace('_immediate', '')
            phiParams = [f'[{reg[0]}, %l{reg[3]}]' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node
            sourceNode.mappings[identifier] = (llvmType, f'{lastRegUsed+1}', currentNode.id)
            return lastRegUsed+1, llvmType, [f'%t{lastRegUsed+1} = phi {llvmType} {phiParams}'], currentNode.id


def readUnsealedBlock(targetRegister:int, identifier:str, currentNode:CFG_Node, sourceNode:CFG_Node) -> Tuple[int, str, list[str], str]:
    # create phi node with values in prev blocks
    if len(currentNode.prevNodes) == 1:
        prevNode = currentNode.prevNodes[0]
        return readUnsealedBlock(targetRegister, identifier, prevNode, sourceNode)

    possibleSrcRegisters = [readVariable(targetRegister, identifier, node, sourceNode) for node in currentNode.prevNodes]
    
    phiParams = []

    if 'immediate' in possibleSrcRegisters[0][1]:
        llvmType = possibleSrcRegisters[0][1].split('_')[0]
    else:
        llvmType = possibleSrcRegisters[0][1]

    for reg in possibleSrcRegisters:
        val = reg[0]
        if 'immediate' not in reg[1]:
            val = f'%t{val}'
        phiParams.append(f'[{val}, %l{reg[3]}]')
    phiParams = ', '.join(phiParams)

    # map variable to phi node
    # currentNode.mappings[identifier] = (llvmType, lastRegUsed+1, currentNode.id)
    return targetRegister, llvmType, [f'%t{targetRegister} = phi {llvmType} {phiParams}'], currentNode.id


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = env[currentID][1].typeID

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

        if currentID in env and env[currentID][0]:
            instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
        else:
            instruction = f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i32 or %struct.__*
    outputCode.append(f'%t{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %t{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    leftOpReg, leftLLVMType, leftOpCode = expressionToSSA(lastRegUsed, binop.left_expression, env, types, functions, currentNode)

    if 'immediate' not in leftLLVMType:
        lastRegUsed = leftOpReg
        if type(leftOpReg) == int: # '%t' not in leftOpReg:
            leftOpReg = f'%t{leftOpReg}'  
    else:
        leftLLVMType = leftLLVMType.split('_')[0]

    rightOpReg, rightLLVMType, rightOpCode = expressionToSSA(lastRegUsed, binop.right_expression, env, types, functions, currentNode)

    if 'immediate' not in rightLLVMType:
        lastRegUsed = rightOpReg
        if type(rightOpReg) == int:  # '%t' not in rightOpReg 
            rightOpReg = f'%t{rightOpReg}'
    else:
        rightLLVMType = rightLLVMType.split('_')[0]

    # == != <= < > >= - + * / || &&
    match binop.operator:
        case '==':
            op = 'icmp eq i32'
        case '!=':
            op = 'icmp ne i32'
        case '<=':
            op = 'icmp sle i32'
        case '<':
            op = 'icmp slt i32'
        case '>=':
            op = 'icmp sge i32'
        case '>':
            op = 'icmp sgt i32'
        case '-':
            op = 'sub i32'
        case '+':
            op = 'add i32'
        case '*':
            op = 'mul i32'
        case '/':
            op = 'div i32'
        case '||':
            op = 'or i32'
        case '&&':
            op = 'and i32'

    instructions = []
    instructions.extend(leftOpCode)
    instructions.extend(rightOpCode)
    instructions.append(f'%t{lastRegUsed + 1} = {op} {leftOpReg}, {rightOpReg}')

    return (lastRegUsed + 1, 'i32', instructions)


def unaryToSSA(lastRegUsed:int, exp:m_unary, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    operandReg, operandType, operandCode = expressionToSSA(lastRegUsed, exp.operand_expression, env, types, functions, currentNode)

    if 'immediate' not in operandType:
        lastRegUsed = operandReg
        if type(operandReg) == int:  # '%t' not in rightOpReg 
            operandReg = f'%t{operandReg}'
    else:
        operandType = operandType.split('_')[0]

    match exp.operator:
        case '!':
            op = f'xor i32 1'
        case '-':
            op = f'mul i32 -1'
        
    operandCode.append(f'%t{operandReg + 1} = {op}, {operandReg}')
    return operandReg+1, 'i32', operandCode


def invocationToSSA(lastRegUsed:int, exp:m_invocation, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    parameters = []
    instructions = []
    for expression in exp.args_expressions:
        paramReg, paramType, paramCode = expressionToSSA(lastRegUsed, expression, env, types, functions, currentNode)
        if 'immediate' in paramType:
            tp = paramType.split('_')[0]
            parameters.append(f'{tp} {paramReg}')
        else:
            if type(paramReg) != int:
                parameters.append(f'{paramType} {paramReg}')
            else:
                parameters.append(f'{paramType} %t{paramReg}')

            instructions.extend(paramCode)  
            lastRegUsed = paramReg

    targetReg = lastRegUsed + 1
    returnTypeID = getLLVMType(functions[exp.id.identifier][0].typeID)
    funID = exp.id.identifier        
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    instructions.append(f'%t{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return targetReg, returnTypeID, instructions


# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)


# Placeholder for phi node
# ASK PROFESSOR ABOUT THIS ON THURSDAY
class phi:
    def __init__(self, lst:list, complete = False):
        self.possibleValues = lst
    def getPlaceHolder():
        return 'i32', 0