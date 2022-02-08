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
def statementToSSA(lastRegUsed:int, stmt, mappings:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, dict, list[str]]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, mappings, types, functions, currentNode)
        case m_print():
            pass
        case m_delete():
            pass
        case m_ret():
            pass
        case m_invocation():
            pass


def assignToSSA(lastRegUsed:int, assign:m_assignment, mappings:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, dict, list[str]]:
    exprReg, exprType, mappings, exprCode = expressionToLLVM(lastRegUsed, assign.source_expression, mappings, types, functions, currentNode)
    targetStrings = [mid.identifier for mid in assign.target_ids]
    key = '.'.join(targetStrings)
    mappings[key] = (exprType, exprReg)

    return exprReg, mappings, exprCode
    

# returns a tuple containing (resultReg, llvmType, mappings within block, SSA LLVM code)
def expressionToLLVM(lastRegUsed:int, expr, mappings:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, dict, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, mappings, types, functions, currentNode)
        case m_num() | m_bool():
            return lastRegUsed+1, 'i32', mappings, [f'%r{lastRegUsed+1} = i32 {expr.val}']
        case m_new_struct():
            pass
        case m_null():
            pass
        case m_invocation():
            pass
        case m_read():
            pass
        case m_unary():
            pass
        case m_dot():
            pass
        case m_id():
            if expr.identifier in mappings:
                return mappings[expr.identifier][1], mappings[expr.identifier][0], mappings, []
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
                    prevMappings = currentNode.previousBlocks[0].mappings
                    return expressionToLLVM(lastRegUsed, expr, prevMappings, types, functions, currentNode.previousBlocks[0])
                else:
                    # create phi node with values in prev blocks
                    # map variable to phi node
                    pass
                pass


def readVariable(identifier:str, currentNode:CFG_Node):
    if 


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, mappings:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, dict, list[str]]:
    leftOpReg, leftLLVMType, mappings, leftOpCode = expressionToLLVM(lastRegUsed, binop.left_expression, mappings, types, functions, currentNode)
    rightOpReg, rightLLVMType, mappings, rightOpCode = expressionToLLVM(leftOpReg, binop.right_expression, mappings, types, functions, currentNode)

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
            op = 'or i32'

    instructions = []
    targetReg = rightOpReg + 1
    instructions.extend(leftOpCode)
    instructions.extend(rightOpCode)
    instructions.append(f'%r{targetReg} = {op} %r{leftOpReg}, %r{rightOpReg}')

    return (targetReg, 'i32', mappings, instructions)