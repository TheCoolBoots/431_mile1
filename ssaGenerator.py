from typing import Dict, Tuple
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import *
from generateLLVM import getLLVMType

def tmp(prog:m_prog):
    # create a function node for each function
    functionList = generate_CFG_Prog_Handler(prog) # this is a list of function nodes


    # generate globals, generate top_env, generate types
    # may need a new function for getting declarations in the global env
    lastReg = 0
    globalDeclarations = []
    for dec in prog.global_declarations:
        # get the list of code from the current declaration
        declarationList = dec.getSSA(lastReg, prog.getTypeSizes())  # return list of strings
        lastReg += 1  # increment by just 1?

        # extend the globalDeclarations list of code
        globalDeclarations.extend(declarationList)



    # getTopEnv(self, includeLineNum=True)
    # get the dictionary of string to type in the global environment
    globalTopEnv = prog.getTopEnv(False)


    # will need to step through each statement in each block in each function
    # convert to llvm code with - statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node)
    for fun in functionList:
        currBlock = fun.firstNode # get the first block in a function


        # make dict of traversed nodes
        nodeDict = {}

        # make queue for traversing nodes
        queue = []

        # start off the queue
        queue.append(currBlock)

        # step through each block of current tree and convert statements to SSA LLVM
        while queue != []:
            # take first item from the queue
            currBlock = queue.pop(0)

            # check if youve already looked at this node
            if currBlock in nodeDict:
                continue

            # add the current node to the visited dict
            nodeDict[currBlock] = True

            # will need to include global environment in the generateSSA function
            # _generateSSA(currentNode: CFG_Node, types, functions) : return code, currentNode.mappings
            tempCode, mappings = _generateSSA(currBlock, prog.getTypes(), WILLBEAFUNCTION(), globalTopEnv)

            # update the ast code to be replaced with SSA LLVM code
            currBlock.code = tempCode
            currBlock.mappings = mappings # YES?

            # check if there are any next nodes, add them if so
            for tempNode in currBlock.nextBlocks:
                queue.append(tempNode)


            # anything else??




    # generate llvm code for functions


    # look at if and while loops

    pass

def generateSSA(rootNode:CFG_Node, env, types, functions):
    # whiles and ifs
    
    pass


# top_env structure: {str: m_type} 
# types structure: {str: list[m_declaration]}
# functions structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types

def _generateSSA(currentNode: CFG_Node, top_env:dict, types:dict, functions:dict):
    code = []
    lastRegUsed = 0
    statements = currentNode.code
    for statement in statements:
        lastRegUsed, llvmType, newCode = statementToSSA(lastRegUsed, statement, top_env, types, functions, currentNode)
        code.extend(newCode)

    return code, currentNode.mappings

# env maps strings to types {str: str(typeID)}
# r_ = load type[id] @z
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# returns a tuple containing (mappings within block, SSA LLVM code)
def statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, types, functions, currentNode)
        case m_print():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, types, functions, currentNode)
            if type(exprCode) == list:
                instruction = f'%{exprReg + 1} = call i32 @printf("%d", %{exprReg})'
                exprCode.append(instruction)
                return exprReg + 1, 'i32', exprCode
        case m_delete():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, types, functions, currentNode)
            if type(exprReg) != str:
                lastRegUsed = exprReg
            exprCode.extend([f'%{lastRegUsed + 1} = bitcast {exprType} %{exprReg} to i8*',
                            f'call void @free(%{lastRegUsed + 1})'])
            currentNode.mappings.pop(exprReg)
            return lastRegUsed + 1, 'void', exprCode
        case m_ret():
            return retToSSA(lastRegUsed, stmt, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized structure:{other}')
            return -1, -1, -1


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        return (lastRegUsed, 'void', [f'ret void'])

    returnReg, retType, returnCode = expressionToLLVM(lastRegUsed, ret.expression, types, functions, currentNode)
    if(retType == 'void'):
        returnCode.append(f'ret {retType}')
    else:
        returnCode.append(f'ret {retType} %{returnReg}')

    return (returnReg, retType, returnCode)


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, assign.source_expression, types, functions, currentNode)
    if type(exprReg) == int:
        lastRegUsed = exprReg
    targetStrings = [mid.identifier for mid in assign.target_ids]

    if len(targetStrings) == 1:
        # if the target is in the top_env, that means it is either a global var or local struct
        #       if global var, use @
        #       if local struct, use normal
        if targetStrings[0] in env:
            if env[targetStrings[0]] == m_type('int') or env[targetStrings[0]] == m_type('bool'):
                return lastRegUsed, env[targetStrings[0]], [f'store {exprType} %{exprReg}, i32* @{targetStrings[0]}']

        # if it is not in top_env, it is a local variable and is dealt with through SSA form

        currentNode.mappings[targetStrings[0]] = (exprType, exprReg, 'placeholder')
        return exprReg, exprType, exprCode
    else:
        currentID = assign.target_ids[0].identifier
        currentIDTypeID = currentNode.mappings[currentID][2]
        
        nested = False
        for accessedm_id in assign.target_ids[1:]:
            nested = True
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

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
    

# returns a tuple containing (resultReg, llvmType, mappings within block, SSA LLVM code)
def expressionToLLVM(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, types, functions, currentNode)
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
            return invocationToSSA(lastRegUsed, expr, types, functions, currentNode)
        case m_read():
            return lastRegUsed+2, 'i32', [f'%{lastRegUsed+2} = alloc i32', f'%{lastRegUsed+1} = call i32 @scanf("%d", %{lastRegUsed+2}*)']
        case m_unary():
            pass
        case m_dot():
            return dotToSSA(lastRegUsed, expr, types, functions, currentNode)
        case m_id():
            llvmType, resultReg = readVariable(lastRegUsed, expr.identifier, currentNode)
            return resultReg, llvmType, []
        case other:
            print(f'ERROR: unrecognized expression: {other}')


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = currentNode.mappings[currentID][2]

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

        instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i32 or %struct.__*
    outputCode.append(f'%{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)


# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)


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
            return readVariable(identifier, prevNode)
        else:
            # create phi node with values in prev blocks
            possibleRegisters = [readVariable(identifier, node) for node in currentNode.previousBlocks]
            llvmType = possibleRegisters[0][1]
            phiParams = [f'{reg[1]} %{reg[0]}' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node
            currentNode.mappings[identifier] = (llvmType, lastRegUsed+1)
            return (lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = phi({phiParams})'])

# Placeholder for phi node
# ASK PROFESSOR ABOUT THIS ON THURSDAY
class phi:
    def __init__(self, lst:list, complete = False):
        self.possibleValues = lst
    def getPlaceHolder():
        return 'i32', 0

# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    leftOpReg, leftLLVMType, leftOpCode = expressionToLLVM(lastRegUsed, binop.left_expression, types, functions, currentNode)
    rightOpReg, rightLLVMType, rightOpCode = expressionToLLVM(leftOpReg, binop.right_expression, types, functions, currentNode)

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
        params.append(expressionToLLVM(lastRegUsed, expression, types, functions, currentNode))
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