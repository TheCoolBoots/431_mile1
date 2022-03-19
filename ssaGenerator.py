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
# returns the last register used
def statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> int:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case m_print():
            lastRegUsed, exprVal, exprType = expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            
            if not stmt.endl:
                instruction = f'%t{lastRegUsed + 1} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 {exprVal})'
            else:
                instruction = f'%t{lastRegUsed + 1} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.str.1, i64 0, i64 0), i32 {exprVal})'
            currentNode.llvmCode.append(instruction)
            return lastRegUsed + 1
        case m_delete():
            lastRegUsed, exprVal, exprType= expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
 
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = bitcast {exprType} {exprVal} to i8*',
                            f'call void @free(i8* %t{lastRegUsed + 1})'])
            # env.pop(exprReg)
            return lastRegUsed + 1
        case m_invocation():
            return invocationToSSA(lastRegUsed, stmt, env, types, functions, currentNode, True)
        case m_ret():
            return retToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized m_statement:{other}')
            return lastRegUsed


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        currentNode.llvmCode.append(f'ret void')
        return lastRegUsed

    lastRegUsed, retVal, retType = expressionToSSA(lastRegUsed, ret.expression, env, types, functions, currentNode)

    if retType == 'void':
        currentNode.llvmCode.append(f'ret void')
    else: 
        currentNode.llvmCode.append(f'ret {currentNode.llvmRetType} {retVal}')

    return lastRegUsed


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    lastRegUsed, exprVal, exprType = expressionToSSA(lastRegUsed, assign.source_expression, env, types, functions, currentNode)

    targetStrings = [mid.identifier for mid in assign.target_ids]

    rootID = targetStrings[0]
    readVarRet = readVariable(lastRegUsed, rootID, currentNode)

    # variable is a global variable
    if readVarRet == None:
        currentIDTypeID = env[rootID][1].typeID
        currentID = f'@{rootID}'
        
        for accessedm_id in targetStrings[1:]:
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

            if currentID in env and env[currentID][0]:
                currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load %struct.{currentIDTypeID}*, %struct.{currentIDTypeID}** {currentID}')
                currentNode.llvmCode.append(f'%t{lastRegUsed + 2} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %t{lastRegUsed + 1}, i32 0, i32 {accessedIDmemNum}')
                currentID = f'%t{lastRegUsed + 2}'
                lastRegUsed += 2

            else:
                currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
                currentID = f'%t{lastRegUsed + 1}'
                lastRegUsed += 1
                
            currentIDTypeID = accessedTypeID

        llvmType = getLLVMType(currentIDTypeID)
        currentNode.llvmCode.append(f'store {llvmType} {exprVal}, {llvmType}* {currentID}')
        return lastRegUsed

    lastRegUsed, currentID, llvmType, lastLabel = readVarRet

    # if the variable is a struct
    if llvmType[0] == '%':
        currentIDTypeID = llvmType[8:-1]

        for id in targetStrings[1:]:
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(id, types[currentIDTypeID])

            currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
            currentID = f'%t{lastRegUsed + 1}'
            lastRegUsed += 1
            currentIDTypeID = accessedTypeID
    
    
        llvmType = getLLVMType(currentIDTypeID)
        if len(targetStrings) > 1:
            currentNode.llvmCode.append(f'store {llvmType} {exprVal}, {llvmType}* {currentID}')
        else:
            currentNode.mappings[targetStrings[0]] = (exprType, exprVal, currentNode.id)
        return lastRegUsed
    else:
        currentNode.mappings[targetStrings[0]] = (exprType, exprVal, currentNode.id)
        return lastRegUsed

        
    

# returns a tuple containing (resultReg, llvmType)
def expressionToSSA(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, str]:
    match expr:
        case m_id():
            readRet = readVariable(lastRegUsed, expr.identifier, currentNode)

            # if id is a global variable
            if readRet == None:
                llvmType = getLLVMType(env[expr.identifier][1].typeID)
                currentNode.llvmCode.extend([f'%t{lastRegUsed+1} = load {llvmType}, {llvmType}* @{expr.identifier}'])
                return lastRegUsed+1, f'%t{lastRegUsed+1}', llvmType
            
            # handle with SSA form
            return readRet[0], readRet[1], readRet[2]
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, env, types, functions, currentNode)
        case m_num():
            return lastRegUsed, expr.val, 'i32'
        case m_bool():
            return lastRegUsed, int(expr.val), 'i1'
        case m_new_struct():
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = call i8* @malloc(i32 {len(types[expr.struct_id.identifier]) * 4})',
                 f'%t{lastRegUsed + 2} = bitcast i8* %t{lastRegUsed + 1} to %struct.{expr.struct_id.identifier}*'])
            return lastRegUsed+2, f'%t{lastRegUsed + 2}', f'%struct.{expr.struct_id.identifier}*'
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return lastRegUsed, 'null', 'null'
        case m_invocation():
            return invocationToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_read():
            currentNode.llvmCode.extend([f'%t{lastRegUsed + 1} = alloca i32',
                        f'%t{lastRegUsed+2} = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* %t{lastRegUsed + 1})',
                        f'%t{lastRegUsed+3} = load i32, i32* %t{lastRegUsed+1}'])
            return lastRegUsed+3, f'%t{lastRegUsed+3}', 'i32'
        case m_unary():
            return unaryToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_dot():
            return dotToSSA(lastRegUsed, expr, env, types, functions, currentNode)

        case other:
            print(f'ERROR: unrecognized expression: {other}')


# mappings structure = {str id: (str llvmType, value, int nodeID)}
# returns lastRegUsed, llvmType, preceeding label
def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node) -> Tuple[int, str, str, int]:
    if identifier in currentNode.mappings:
        return lastRegUsed, currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], currentNode.id
                
    else:
        if not currentNode.sealed:
            # guard block isnt sealed yet, therefore it goes into this one
            if type(lastRegUsed) != int:
                lastRegUsed = int(lastRegUsed[2:])
            
            # TODO: structs won't be i32
            # NEED TO GET THE LLVMTYPE OF STRUCTS IN MAPPINGS SOMEHOW
            if identifier not in currentNode.progRootNode.mappings[identifier]:
                return None
            identifierType = currentNode.progRootNode.mappings[identifier][0]
            currentNode.mappings[identifier] = (identifierType, f'%t{lastRegUsed+1}', currentNode.id)
            if len(currentNode.llvmCode) > 0 and currentNode.llvmCode[0][-1] == ':':
                currentNode.llvmCode.insert(1, f'{lastRegUsed+1}-{currentNode.id}-{identifier}-*')
            else:
                currentNode.llvmCode.insert(0, f'{lastRegUsed+1}-{currentNode.id}-{identifier}-*')
            return lastRegUsed+1, f'%t{lastRegUsed+1}', identifierType, currentNode.id
        elif len(currentNode.prevNodes) == 0:
            # val is undefined
            # should never encounter this case
            # print('ERROR: hit the undefined part for readVariable')
            pass
        elif len(currentNode.prevNodes) == 1:
            # call expressionToLLVM with expr and prev block's mappings
            prevNode = currentNode.prevNodes[0]
            lastRegUsed, varValue, llvmType, discard = readVariable(lastRegUsed, identifier, prevNode)
            return lastRegUsed, varValue, llvmType, currentNode.id
        else:
            # create phi node with values in prev blocks
            possibleRegisters = []
            for node in currentNode.prevNodes:
                possibleRegisters.append(readVariable(lastRegUsed, identifier, node))
                lastRegUsed = possibleRegisters[-1][0]
            llvmType = possibleRegisters[0][2]
            phiParams = [f'[{reg[1]}, %l{reg[3]}]' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node


            # if the line at index 0 is the block label, then put it at index 1 instead
            if len(currentNode.llvmCode) > 0 and currentNode.llvmCode[0][-1] == ':':
                currentNode.llvmCode.insert(1, f'%t{lastRegUsed+1} = phi {llvmType} {phiParams}')
            else:
                currentNode.llvmCode.insert(0, f'%t{lastRegUsed+1} = phi {llvmType} {phiParams}')

            currentNode.mappings[identifier] = (llvmType, f'%t{lastRegUsed+1}', currentNode.id)

            return lastRegUsed+1, f'%t{lastRegUsed+1}', llvmType, currentNode.id


def readUnsealedBlock(lastRegUsed:int, node:CFG_Node, identifier:str, targetReg:int) -> Tuple[str, int]:
    possibleSrcRegisters = []
    for n in node.prevNodes:
        possibleSrcRegisters.append(readVariable(lastRegUsed, identifier, n))
        lastRegUsed = possibleSrcRegisters[-1][0]
        
    # print(possibleSrcRegisters)
    phiParams = []
    for reg in possibleSrcRegisters:
        phiParams.append(f'[{reg[1]}, %l{reg[3]}]')
    phiParams = ', '.join(phiParams)

    return lastRegUsed, f'%t{targetReg} = phi {possibleSrcRegisters[0][2]} {phiParams}'


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str ,str]:
    rootID = expression.ids[0].identifier
    readVarRet = readVariable(lastRegUsed, rootID, currentNode)

    # variable is a global variable in the top env
    if readVarRet == None:
        currentID = rootID
        currentIDTypeID = env[currentID][1].typeID
        
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(expression.ids[1].identifier, types[currentIDTypeID])

        # load the pointer to struct from pointer pointer
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load %struct.{currentIDTypeID}*, %struct.{currentIDTypeID}** @{currentID}')
        currentNode.llvmCode.append(f'%t{lastRegUsed + 2} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %t{lastRegUsed + 1}, i32 0, i32 {accessedIDmemNum}')
        currentID = f'%t{lastRegUsed + 2}'
        lastRegUsed += 2
        currentIDTypeID = accessedTypeID

        for accessedm_id in expression.ids[2:]:
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id.identifier, types[currentIDTypeID])

            currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
            currentID = f'%t{lastRegUsed + 1}'
            lastRegUsed += 1
                
            currentIDTypeID = accessedTypeID

        llvmType = getLLVMType(currentIDTypeID)
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load {llvmType}, {llvmType}* {currentID}')
        return lastRegUsed + 1, f'%t{lastRegUsed + 1}' , llvmType


    # variable is a parameter or declared locally
    lastRegUsed, currentID, llvmType, lastLabel = readVarRet
    # llvmType should always be in form %struct.__*
    currentIDTypeID = llvmType[8:-1]

    for id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(id.identifier, types[currentIDTypeID])

        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* {currentID}, i32 0, i32 {accessedIDmemNum}')
        currentID = f'%t{lastRegUsed + 1}'
        lastRegUsed += 1
        currentIDTypeID = accessedTypeID

    llvmType = getLLVMType(currentIDTypeID)
    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = load {llvmType}, {llvmType}* {currentID}')
    return lastRegUsed+1, f'%t{lastRegUsed + 1}', llvmType


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    lastRegUsed, leftOperand, leftLLVMType = expressionToSSA(lastRegUsed, binop.left_expression, env, types, functions, currentNode)

    lastRegUsed, rightOperand, rightLLVMType = expressionToSSA(lastRegUsed, binop.right_expression, env, types, functions, currentNode)

    # == != <= < > >= - + * / || &&
    match binop.operator:
        case '==':
            op = 'icmp eq'
            retType = 'i1'
        case '!=':
            op = 'icmp ne'
            retType = 'i1'
        case '<=':
            op = 'icmp sle'
            retType = 'i1'
        case '<':
            op = 'icmp slt'
            retType = 'i1'
        case '>=':
            op = 'icmp sge'
            retType = 'i1'
        case '>':
            op = 'icmp sgt'
            retType = 'i1'
        case '-':
            op = 'sub'
            retType = 'i32'
        case '+':
            op = 'add'
            retType = 'i32'
        case '*':
            op = 'mul'
            retType = 'i32'
        case '/':
            op = 'sdiv'
            retType = 'i32'
        case '||':
            op = 'or'
            retType = 'i1'
        case '&&':
            op = 'and'
            retType = 'i1'

    
    if leftLLVMType == 'null':
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = {op} {rightLLVMType} {leftOperand}, {rightOperand}')
    else:
        currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = {op} {leftLLVMType} {leftOperand}, {rightOperand}')
        

    return lastRegUsed + 1, f'%t{lastRegUsed + 1}', retType


def unaryToSSA(lastRegUsed:int, exp:m_unary, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str]:
    lastRegUsed, operand, operandType = expressionToSSA(lastRegUsed, exp.operand_expression, env, types, functions, currentNode)

    match exp.operator:
        case '!':
            op = f'xor i1 1'
        case '-':
            op = f'mul i32 -1'
        
    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = {op}, {operand}')
    return lastRegUsed+1, f'%t{lastRegUsed + 1}', 'i32'


def invocationToSSA(lastRegUsed:int, exp:m_invocation, env:dict, types:dict, functions:dict, currentNode:CFG_Node, statement = False) -> Tuple[int, str]:
    parameters = []
    instructions = []
    for expression in exp.args_expressions:
        lastRegUsed, paramVal, paramType = expressionToSSA(lastRegUsed, expression, env, types, functions, currentNode)
        parameters.append(f'{paramType} {paramVal}')

    returnTypeID = getLLVMType(functions[exp.id.identifier][0].typeID)
    funID = exp.id.identifier        
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
        
    if statement:
        currentNode.llvmCode.append(f'call {returnTypeID} @{funID}({parameters})')
        return lastRegUsed

    currentNode.llvmCode.append(f'%t{lastRegUsed + 1} = call {returnTypeID} @{funID}({parameters})')
    return lastRegUsed + 1, f'%t{lastRegUsed + 1}', returnTypeID


# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id.identifier == id:
            return (i, decl.type.typeID)

