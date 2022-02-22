from typing import Dict, Tuple
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import *
from generateLLVM import getLLVMType
from test_cfg_generator import *



# top_env structure: {str: (bool, m_type)}              where bool == true if global, false if local 
# types structure: {str: list[m_declaration]}
# functions structure: {str: (m_type, list[m_type])}    maps funID -> return type, param types
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# functions structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types
# {str funName: (m_type returnType, list[m_type] paramTypes)}


def generateSSA(currentNode: CFG_Node, top_env:dict, types:dict, functions:dict):
    code = []
    lastRegUsed = currentNode.lastRegUsed
    statements = currentNode.code

    # print("ALL statements: " + str(statements))

    for statement in statements:
        lastRegUsed, llvmType, newCode = statementToSSA(lastRegUsed, statement, top_env, types, functions, currentNode)

        if newCode == -1:
            # print("currStatement: " + str(statement))

            # NEED TO WRITE CODE TO DEAL WITH UNARY, BINOP, AND BOOL HERE
            code.extend(["GUARD CODE PLACEHOLDER"])

            continue  # REMOVE continue ????

        code.extend(newCode)

    return lastRegUsed, code, currentNode.mappings


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
            if type(exprCode) == list:
                instruction = f'%{exprReg + 1} = call i32 @printf("%d", %{exprReg})'
                exprCode.append(instruction)
                return exprReg + 1, 'i32', exprCode
        case m_delete():
            exprReg, exprType, exprCode = expressionToSSA(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            if type(exprReg) != str:
                lastRegUsed = exprReg
            exprCode.extend([f'%{lastRegUsed + 1} = bitcast {exprType} %{exprReg} to i8*',
                            f'call void @free(%{lastRegUsed + 1})'])
            # env.pop(exprReg)
            return lastRegUsed + 1, 'void', exprCode
        case m_ret():
            return retToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized structure:{other}')
            return lastRegUsed, -1, -1


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        return (lastRegUsed, 'void', [f'ret void'])

    returnReg, retType, returnCode = expressionToSSA(lastRegUsed, ret.expression, env, types, functions, currentNode)
    if(retType == 'void'):
        returnCode.append(f'ret {retType}')
    else:
        returnCode.append(f'ret {retType} %{returnReg}')

    return (returnReg, retType, returnCode)


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    exprReg, exprType, exprCode = expressionToSSA(lastRegUsed, assign.source_expression, env, types, functions, currentNode)
    if type(exprReg) == int:
        lastRegUsed = exprReg
    targetStrings = [mid.identifier for mid in assign.target_ids]

    if len(targetStrings) == 1:
        # if the target is in the top_env, that means it is either a global var or global/local struct
        #       if global var, use @
        #       if local struct, use normal
        if targetStrings[0] in env:
            if env[targetStrings[0]] == m_type('int') or env[targetStrings[0]] == m_type('bool'):
                exprCode.append(f'store {exprType} %{exprReg}, i32* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # if struct is a global struct
            elif env[targetStrings[0]][0]:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} %{exprReg}, {typeStr}* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # struct is a locally defined struct
            else:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} %{exprReg}, {typeStr}* %{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode

        # if it is not in top_env, it is a local variable and is dealt with through SSA form
        currentNode.mappings[targetStrings[0]] = (exprType, exprReg, 'placeholder')
        return exprReg, exprType, exprCode
    else:
        currentID = assign.target_ids[0].identifier
        currentIDTypeID = env[currentID][1].typeID
        
        nested = False
        for accessedm_id in assign.target_ids[1:]:
            nested = True
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

            if currentID in env and env[currentID][0]:
                instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
            else:
                instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
            exprCode.append(instruction)

            currentID = lastRegUsed + 1
            currentIDTypeID = accessedTypeID
            lastRegUsed += 1


        if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
            exprCode.append(f'store i32 %{exprReg}, i32* %{currentID}')
            return lastRegUsed, 'i32', exprCode
        #(f'store %struct.s1* %1, %struct.s1** %2')
        else:
            if nested:
                llvmType = getLLVMType(currentIDTypeID)
                exprCode.append(f'store {llvmType} %{exprReg}, {llvmType}* %{currentID}')
                return lastRegUsed, llvmType, exprCode
            else:
                exprCode.append(f'%{currentID} = %{exprReg}')
                return lastRegUsed, getLLVMType(currentIDTypeID), exprCode
    

# returns a tuple containing (resultReg, llvmType, SSA LLVM code)
def expressionToSSA(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, env, types, functions, currentNode)
        case m_num() | m_bool():
            return lastRegUsed+1, 'i32', [f'%{lastRegUsed+1} = i32 {expr.val}']
        case m_new_struct():
            # ASK PROFESSOR ABOUT THIS ON TUESDAY
            code = [f'%{lastRegUsed + 1} = call i8* @malloc({len(types[expr.struct_id.identifier]) * 4})',
                 f'%{lastRegUsed + 1} = bitcast i8* %{lastRegUsed + 1} to %struct.{expr.struct_id.identifier}*']
            return lastRegUsed+1, f'%struct.{expr.struct_id.identifier}*', code
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return lastRegUsed+1, 'i32', [f'%{lastRegUsed+1} = i32 0']
        case m_invocation():
            return invocationToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_read():
            return lastRegUsed+2, 'i32', [f'%{lastRegUsed+2} = alloc i32', f'%{lastRegUsed+1} = call i32 @scanf("%d", %{lastRegUsed+2}*)']
        case m_unary():
            pass
        case m_dot():
            return dotToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_id():
            if expr.identifier in env:
                # if id is a global variable
                if env[expr.identifier][0]:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = load {llvmType}* @{expr.identifier}']
                else:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = load {llvmType}* %{expr.identifier}']
            return readVariable(lastRegUsed, expr.identifier, currentNode)
        case other:
            print(f'ERROR: unrecognized expression: {other}')


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = env[currentID][1].typeID

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

        if currentID in env and env[currentID][0]:
            instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
        else:
            instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i32 or %struct.__*
    outputCode.append(f'%{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)


# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if identifier in currentNode.mappings:
        return currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], []
    else:
        if not currentNode.sealed:
            currentNode.mappings[identifier] = ('?', lastRegUsed+1)
            return lastRegUsed+1, '?', [f'%{lastRegUsed + 1} = phi(_)']
        elif len(currentNode.previousBlocks) == 0:
            # val is undefined
            # should never encounter this case
            pass
        elif len(currentNode.previousBlocks) == 1:
            # call expressionToLLVM with expr and prev block's mappings
            prevNode = currentNode.previousBlocks[0]
            return readVariable(lastRegUsed, identifier, prevNode)
        else:
            # create phi node with values in prev blocks
            possibleRegisters = [readVariable(lastRegUsed, identifier, node) for node in currentNode.previousBlocks]
            llvmType = possibleRegisters[0][1]
            phiParams = [f'{reg[1]} %{reg[0]}' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node
            currentNode.mappings[identifier] = (llvmType, lastRegUsed+1)
            return (lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = phi({phiParams})'])


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    leftOpReg, leftLLVMType, leftOpCode = expressionToSSA(lastRegUsed, binop.left_expression, env, types, functions, currentNode)
    rightOpReg, rightLLVMType, rightOpCode = expressionToSSA(leftOpReg, binop.right_expression, env, types, functions, currentNode)

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
    targetReg = rightOpReg + 1
    instructions.extend(leftOpCode)
    instructions.extend(rightOpCode)
    instructions.append(f'%{targetReg} = {op} %{leftOpReg}, i32 %{rightOpReg}')

    return (targetReg, 'i32', instructions)


def invocationToSSA(lastRegUsed:int, exp:m_invocation, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    params = []
    for expression in exp.args_expressions:
        params.append(expressionToSSA(lastRegUsed, expression, env, types, functions, currentNode))
        lastRegUsed = params[-1][0]

    targetReg = params[-1][0] + 1
    returnTypeID = getLLVMType(functions[exp.id.identifier][0].typeID)
    funID = exp.id.identifier

    parameters = []
    instructions = []

    for paramReg, paramType, paramCode in params:
        parameters.append(f'{paramType} %{paramReg}')
        instructions.extend(paramCode)
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    instructions.append(f'%{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return (targetReg, returnTypeID, instructions)


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