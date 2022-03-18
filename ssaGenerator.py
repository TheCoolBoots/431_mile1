from typing import Tuple
from ast_class_definitions import *
from cfg_generator import CFG_Node
from generateLLVM import getLLVMType


# top_env structure: {str: (bool, m_type)}              where bool == true if global, false if local 
# types structure: {str: list[m_declaration]}
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# functions structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types
# {str funName: (m_type returnType, list[m_type] paramTypes)}


# env maps strings to types {str: bool, str(typeID)}
# r_ = load type[id] @z
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# returns a tuple containing (mappings within block, SSA LLVM code)
def statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case m_print():
            exprReg, exprType = expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            
            if 'immediate' not in exprType:
                lastRegUsed = exprReg
                exprReg = f'%t{exprReg}'
            else:
                exprType = exprType.split('_')[0]
            
            if not stmt.endl:
                instruction = f'%t{lastRegUsed + 1} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 {exprReg}))'
            else:
                instruction = f'%t{lastRegUsed + 1} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 {exprReg})'
            currentNode.llvmCode.append(instruction)
            return lastRegUsed + 1, 'i32'
        case m_delete():
            exprReg, exprType= expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            
            if 'immediate' not in exprType:
                lastRegUsed = exprReg
                # exprReg = f'%t{exprReg}'
            else:
                exprType = exprType.split('_')[0]
            
            if type(exprReg) != str:
                lastRegUsed = exprReg
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = bitcast {exprType} %t{exprReg} to i8*',
                            f'call void @free(i8* %t{lastRegUsed + 1})'])
            # env.pop(exprReg)
            return lastRegUsed + 1, 'null'
        case m_ret():
            return retToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized structure:{other}')
            return lastRegUsed, -1


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        currentNode.llvmCode.append(f'ret null')
        return lastRegUsed, 'null'

    returnReg, retType = expressionToSSA(lastRegUsed, ret.expression, env, types, functions, currentNode)

    if 'immediate' not in retType:
        returnReg = f'%t{returnReg}'
    else:
        retType = retType.split('_')[0]

    if(retType == 'null'):
        currentNode.llvmCode.append(f'ret null')
    else:
        currentNode.llvmCode.append(f'ret {retType} {returnReg}')

    return returnReg, retType


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    exprReg, exprType = expressionToSSA(lastRegUsed, assign.source_expression, env, types, functions, currentNode)

    if 'immediate' not in exprType:
        lastRegUsed = exprReg
        exprReg = f'%t{exprReg}'
        immediate = False
    else:
        exprType = exprType.split('_')[0]
        immediate = True


    targetStrings = [mid.identifier for mid in assign.target_ids]

    if len(targetStrings) == 1:
        # if the target is in the top_env, that means it is a global variable
        #       if global var, use @
        #       if local struct, use normal
        if targetStrings[0] in env:
            if env[targetStrings[0]] == m_type('int') or env[targetStrings[0]] == m_type('bool'):
                currentNode.llvmCode.append(f'store {exprType} {exprReg}, i32* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]]
            # if struct is a global struct
            elif env[targetStrings[0]][0]:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                currentNode.llvmCode.append(f'store {exprType} {exprReg}, {typeStr}* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]]

        # if it is not in top_env, it is a local variable and is dealt with through SSA form
        if immediate:
            exprType = exprType + '_immediate'
        if type(exprReg) == str:
            exprReg = int(exprReg[2:])
        currentNode.mappings[targetStrings[0]] = (exprType, exprReg, currentNode.id)
        return lastRegUsed, exprType
    else:   # target expression is a struct (A.a.b)
        rootID = targetStrings[0]
        readVarRet = readVariable(lastRegUsed, rootID, currentNode)

        if readVarRet == None:
            currentID = rootID
            currentIDTypeID = env[currentID][1].typeID

            outputCode = []
            
            for accessedm_id in targetStrings[1:]:
                accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

                if currentID in env and env[currentID][0]:
                    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load %struct.{currentIDTypeID}** @{currentID}')
                    currentNode.llvmCode.append(f'%t{lastRegUsed + 2} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %t{lastRegUsed + 1}, i32 0, i32 {accessedIDmemNum}')
                    currentID = lastRegUsed + 2
                    lastRegUsed += 2

                else:
                    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}')
                    currentID = lastRegUsed + 1
                    lastRegUsed += 1
                    
                currentIDTypeID = accessedTypeID

            llvmType = getLLVMType(currentIDTypeID)
            currentNode.llvmCode.append(f'store {llvmType} {exprReg}, {llvmType}* %t{currentID}')
            return lastRegUsed, llvmType

        lookupReg, llvmType, lastLabel = readVarRet

        if 'immediate' not in llvmType:
            lastRegUsed = lookupReg
                # exprReg = f'%t{exprReg}'
        else:
            llvmType = llvmType.split('_')[0]

        currentID = lookupReg
        currentIDTypeID = llvmType[8:-1]
        for id in targetStrings[1:]:
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(id, types[currentIDTypeID])

            currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
            currentID = lastRegUsed + 1
            lastRegUsed += 1
            currentIDTypeID = accessedTypeID
        
        if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
            currentNode.llvmCode.append(f'store i32 {exprReg}, i32* %t{currentID}')
            return lastRegUsed, 'i32'
        else:
            llvmType = getLLVMType(currentIDTypeID)
            currentNode.llvmCode.append(f'store {llvmType} {exprReg}, {llvmType}* %t{currentID}')
            return lastRegUsed, llvmType

        
    

# returns a tuple containing (resultReg, llvmType)
def expressionToSSA(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, env, types, functions, currentNode)
        case m_num():
            return expr.val, 'i32_immediate'
        case m_bool():
            return int(expr.val), 'i1_immediate'
        case m_new_struct():
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = call i8* @malloc({len(types[expr.struct_id.identifier]) * 4})',
                 f'%t{lastRegUsed + 2} = bitcast i8* %t{lastRegUsed + 1} to %struct.{expr.struct_id.identifier}*'])
            return lastRegUsed+2, f'%struct.{expr.struct_id.identifier}*'
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return 'null', 'null_immediate'
        case m_invocation():
            return invocationToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_read():
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = alloca i32',
                        f'%t{lastRegUsed+2} = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t{lastRegUsed + 1})',
                        f'%t{lastRegUsed+3} = load i32, i32* %t{lastRegUsed+1}'])
            return lastRegUsed+3, 'i32'
        case m_unary():
            return unaryToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_dot():
            return dotToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_id():
            if expr.identifier in env:
                # if id is a global variable
                if env[expr.identifier][0]:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    currentNode.llvmCode.extend([f'%t{lastRegUsed+1} = load {llvmType}* @{expr.identifier}'])
                    return lastRegUsed+1, llvmType
                # id is a local variable
                else:
                    # TODO
                    pass
            # handle with SSA form
            exprReg, llvmType, lastLabel = readVariable(lastRegUsed, expr.identifier, currentNode)
            return exprReg, llvmType
        case other:
            print(f'ERROR: unrecognized expression: {other}')


# mappings structure = {str id: (str llvmType, int regNum, int nodeID)}
# returns lastRegUsed, llvmType, preceeding label
def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node) -> Tuple[int, str, int]:
    if identifier in currentNode.mappings:
        if 'immediate' in currentNode.mappings[identifier][0]:
            return currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], currentNode.id
        else:
            if type(currentNode.mappings[identifier][1]) == int:
                return f'%t{currentNode.mappings[identifier][1]}', f'{currentNode.mappings[identifier][0]}_immediate', currentNode.id
            else:
                return f'{currentNode.mappings[identifier][1]}', f'{currentNode.mappings[identifier][0]}_immediate', currentNode.id
                
    else:
        if not currentNode.sealed:
            # guard block isnt sealed yet, therefore it goes into this one
            # structs will never go into mappings so hard coding i32 is fine here
            if type(lastRegUsed) != int:
                lastRegUsed = int(lastRegUsed[2:])
            
            # TODO: structs won't be i32
            currentNode.mappings[identifier] = ('i32', lastRegUsed+1, currentNode.id)
            currentNode.llvmCode.append(f'{lastRegUsed+1}-{currentNode.id}-{identifier}-*')
            return lastRegUsed+1, 'i32', currentNode.id
        elif len(currentNode.prevNodes) == 0:
            # val is undefined
            # should never encounter this case
            pass
        elif len(currentNode.prevNodes) == 1:
            # call expressionToLLVM with expr and prev block's mappings
            prevNode = currentNode.prevNodes[0]
            lastRegUsed, llvmType, discard = readVariable(lastRegUsed, identifier, prevNode)
            return lastRegUsed, llvmType, currentNode.id
        else:
            # create phi node with values in prev blocks
            possibleRegisters = [readVariable(lastRegUsed, identifier, node) for node in currentNode.prevNodes]
            llvmType = possibleRegisters[0][1]
            if 'immediate' in llvmType:
                llvmType = llvmType.replace('_immediate', '')
            phiParams = [f'[{reg[0]}, %l{reg[2]}]' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node
            if type(lastRegUsed) == str:
                lastRegUsed = int(lastRegUsed[2:])
            currentNode.mappings[identifier] = (llvmType, f'{lastRegUsed+1}', currentNode.id)
            currentNode.llvmCode.insert(0, f'%t{lastRegUsed+1} = phi {llvmType} {phiParams}')
            return lastRegUsed+1, llvmType, currentNode.id


def readUnsealedBlock(lastRegUsed:int, node:CFG_Node, identifier:str, targetReg:int) -> Tuple[int, str, int]:
    possibleSrcRegisters = []
    for n in node.prevNodes:
        possibleSrcRegisters.append(readVariable(lastRegUsed, identifier, n))
        if 'immediate' not in possibleSrcRegisters[-1][1]:
            lastRegUsed = possibleSrcRegisters[-1][0]
        
    # print(possibleSrcRegisters)
    phiParams = []
    for reg in possibleSrcRegisters:
        val = reg[0]
        if 'immediate' not in reg[1]:
            val = f'%t{val}'
        phiParams.append(f'[{val}, %l{reg[2]}]')
    phiParams = ', '.join(phiParams)

    if 'immediate' in possibleSrcRegisters[0][1]:
        llvmType = possibleSrcRegisters[0][1].split('_')[0]
    else:
        llvmType = possibleSrcRegisters[0][1]

    return lastRegUsed, f'%t{targetReg} = phi {llvmType} {phiParams}'


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    rootID = expression.ids[0].identifier
    readVarRet = readVariable(lastRegUsed, rootID, currentNode)

    if readVarRet == None:
        currentID = rootID
        currentIDTypeID = env[currentID][1].typeID

        outputCode = []
        
        for accessedm_id in expression.ids[1:]:
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id. identifier, types[currentIDTypeID])

            if currentID in env and env[currentID][0]:
                currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load %struct.{currentIDTypeID}** @{currentID}')
                currentNode.llvmCode.append(f'%t{lastRegUsed + 2} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %t{lastRegUsed + 1}, i32 0, i32 {accessedIDmemNum}')
                currentID = lastRegUsed + 2
                lastRegUsed += 2

            else:
                currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}')
                currentID = lastRegUsed + 1
                lastRegUsed += 1
                
            currentIDTypeID = accessedTypeID

        llvmType = getLLVMType(currentIDTypeID)
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load {llvmType}, {llvmType}* %t{currentID}')
        return lastRegUsed + 1, llvmType

    exprReg, llvmType, lastLabel = readVarRet

    if 'immediate' not in llvmType:
        lastRegUsed = exprReg
    else:
        llvmType = llvmType.split('_')[0]

    if type(exprReg) == int:
        currentID = f'%t{exprReg}'
    else:
        currentID = exprReg

    # llvmType should always be %struct.__*
    currentIDTypeID = llvmType[8:-1]

    for id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(id.identifier, types[currentIDTypeID])

        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
        currentID = f'%t{lastRegUsed + 1}'
        lastRegUsed += 1
        currentIDTypeID = accessedTypeID
    
    if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load i32, i32* {currentID}')
        return lastRegUsed+1, 'i32'
    else:
        llvmType = getLLVMType(currentIDTypeID)
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load {llvmType}, {llvmType}* {currentID}')
        return lastRegUsed+1, llvmType


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    leftOpReg, leftLLVMType = expressionToSSA(lastRegUsed, binop.left_expression, env, types, functions, currentNode)

    if 'immediate' not in leftLLVMType:
        lastRegUsed = leftOpReg
        if type(leftOpReg) == int: # '%t' not in leftOpReg:
            leftOpReg = f'%t{leftOpReg}'  
    else:
        leftLLVMType = leftLLVMType.split('_')[0]

    rightOpReg, rightLLVMType = expressionToSSA(lastRegUsed, binop.right_expression, env, types, functions, currentNode)

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

    if type(lastRegUsed) == str:
        lastRegUsed = int(lastRegUsed[2:])
    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = {op} {leftOpReg}, {rightOpReg}')

    return lastRegUsed + 1, 'i32'


def unaryToSSA(lastRegUsed:int, exp:m_unary, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    operandReg, operandType = expressionToSSA(lastRegUsed, exp.operand_expression, env, types, functions, currentNode)

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
        
    currentNode.llvmCode.append(f'%t{operandReg + 1} = {op}, {operandReg}')
    return operandReg+1, 'i32'


def invocationToSSA(lastRegUsed:int, exp:m_invocation, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    parameters = []
    instructions = []
    for expression in exp.args_expressions:
        paramReg, paramType = expressionToSSA(lastRegUsed, expression, env, types, functions, currentNode)
        if 'immediate' in paramType:
            tp = paramType.split('_')[0]
            parameters.append(f'{tp} {paramReg}')
        else:
            if type(paramReg) != int:
                parameters.append(f'{paramType} {paramReg}')
            else:
                parameters.append(f'{paramType} %t{paramReg}')

            lastRegUsed = paramReg

    targetReg = lastRegUsed + 1
    returnTypeID = getLLVMType(functions[exp.id.identifier][0].typeID)
    funID = exp.id.identifier        
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    currentNode.llvmCode.append(f'%t{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return targetReg, returnTypeID


# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id.identifier == id:
            return (i, decl.type.typeID)
