from typing import Tuple
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import CFG_Node


def generateSSA(rootNode:CFG_Node):
    pass


# def _generateSSA(currentNode:CFG_Node):
#     pass

def _generateSSA(currentNode: CFG_Node):
    code = []
    lastRegUsed = 0
    mappings = {}
    statements = currentNode.code
    for statement in statements:
        lastRegUsed, mappings, newCode = statementToSSA(lastRegUsed, statement, mappings, {}, {}, currentNode)
        code.extend(newCode)

    return '\n'.join(code), mappings


# mappings structure = {str id: (str llvmType, int regNum)}
# returns a tuple containing (mappings within block, SSA LLVM code)
def statementToSSA(lastRegUsed:int, stmt, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, dict, list[str]]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, types, functions, currentNode)
        case m_print():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, types, functions, currentNode)
            if type(exprCode) == list:
                instruction = f'%{exprReg + 1} = call i32 @printf("%d", %{exprReg})'
                exprCode.append(instruction)
                return exprReg + 1, 'i32', exprCode
            else:
                instruction = f'%{exprReg + 1} = call i32 @printf("%d", {exprCode})'
                return exprReg + 1, 'i32', [instruction]

        case m_delete():
            pass
        case m_ret():
            pass
        case m_invocation():
            pass


def assignToSSA(lastRegUsed:int, assign:m_assignment, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, list[str]]:
    exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, assign.source_expression, types, functions, currentNode)
    targetStrings = [mid.identifier for mid in assign.target_ids]
    key = '.'.join(targetStrings)
    currentNode.mappings[key] = (exprType, exprReg)

    return exprReg, exprCode
    

# returns a tuple containing (resultReg, llvmType, mappings within block, SSA LLVM code)
def expressionToLLVM(lastRegUsed:int, expr, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, types, functions, currentNode)
        case m_num() | m_bool():
            return lastRegUsed+1, 'i32', [f'%r{lastRegUsed+1} = i32 {expr.val}']
        case m_new_struct():
            pass
        case m_null():
            pass
        case m_invocation():
            pass
        case m_read():
            pass
        case m_unary():
            return unaryToLLVM(lastRegUsed, expr, types, functions, currentNode)
        case m_dot():
            pass
        case m_id():
            resultReg = readVariable(lastRegUsed, expr.identifier, currentNode)


def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node) -> int:
    if identifier in currentNode.mappings:
        return currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], []
    else:
        if not currentNode.sealed:
            # return a phi node that is incomplete
            # add phi node to incomplete phi nodes
            pass 
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
            # map variable to phi node
            currentNode.mappings[identifier]
            pass
        pass


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
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
    instructions.append(f'%r{targetReg} = {op} %r{leftOpReg}, %r{rightOpReg}')

    return (targetReg, 'i32', mappings, instructions)


# ! -
def unaryToLLVM(lastRegUsed:int, unary:m_unary, types:dict, functions:dict, currentNode:CFG_Node):
    opReg, opLLVMType, opCode = expressionToLLVM(lastRegUsed, unary.operand_expression, types, functions, currentNode)

    # ! =
    match unary.operator:
        case '!':
            op = f'xor i32 1'
        case '-':
            op = f'mul i32 -1'

    instructions = []
    targetReg = opReg + 1
    instructions.extend(opCode)
    instructions.append(f'%r{targetReg} = {op} %r{opReg}')

    return (targetReg, 'i32', instructions)