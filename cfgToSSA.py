from ssaGenerator import expressionToSSA, statementToSSA, readUnsealedBlock
from cfg_generator import generateProgCFGs
from ast_class_definitions import *
from typing import Tuple


# converts an m_prog into an SSA LLVM program
def topSSACompile(prog:m_prog) -> list[str]:
    functionNodes = generateProgCFGs(prog)
    types = prog.getTypes()
    typeSizes = prog.getTypeSizes()

    functions = {}

    typeDefs = [typeDef.getLLVM() for typeDef in prog.types]
    globalDeclarations = [globalDec.getSSAGlobals() for globalDec in prog.global_declarations]

    code = typeDefs
    code.extend(globalDeclarations)

    for fnode in functionNodes:
        functionCode = []

        m_func = fnode.ast
        top_env = prog.getTopEnv(False)
        initialMappings = m_func.getSSALocalMappings()
        fnode.rootNode.mappings = initialMappings
        params = []
        paramTypes = []
        for param in m_func.param_declarations:
            paramTypes.append(param.type)
            params.append(f'{getLLVMType(param.type.typeID)} %{param.id.identifier}')
        params = ', '.join(params)
        if len(params) == 0:
            params = ''
    
        functionCode.append(f'define {getLLVMType(m_func.return_type.typeID)} @{m_func.id.identifier}({params})' + ' {')

        functions[m_func.id.identifier] = (m_func.return_type, paramTypes)

        # register 0 will be reserved for the return value
        sortedNodes = topologicalCFGSort(fnode, False)
        lastRegUsed = firstCFGPass(sortedNodes, top_env, types, functions)
        for n in sortedNodes:
            lastRegUsed = addNodeLabelsAndBranches(lastRegUsed, n, top_env, types, functions)
        
        sealUnsealedBlocks(lastRegUsed, fnode)

        functionCode.extend(buildLLVM(sortedNodes))
        functionCode.append('}')


        code.extend(functionCode)

    return code


def sealUnsealedBlocks(lastRegUsed:int, fnode:Function_CFG) -> int:
    unsealedNodes = fnode.getUnsealedNodes()

    for nodeID, node in unsealedNodes.items():
        for i, line in enumerate(node.llvmCode):
            if line[-1] == '*':
                parts = line.split('-')
                targetReg = int(parts[0])
                nodeID = int(parts[1])
                targetID = parts[2]
                lastRegUsed, newLine = readUnsealedBlock(lastRegUsed, node, targetID, targetReg)
                node.llvmCode[i] = newLine
        unsealedNodes[nodeID].sealed = True
    return lastRegUsed

# generates initial mappings and phi nodes
def firstCFGPass(nodes:list[CFG_Node], top_env, types, functions) -> int:
    lastRegUsed = 0

    for node in nodes:
        for statement in node.ast_statements:
            lastRegUsed = statementToSSA(lastRegUsed, statement, top_env, types, functions, node)

    return lastRegUsed


def buildLLVM(cfgNodes:list[CFG_Node]):
    outputCode = []
    for node in cfgNodes:
        outputCode.extend(node.llvmCode)
    return outputCode


def topologicalCFGSort(functionNode:Function_CFG, returnIDs = True):
    visited = {}
    stack = []

    allNodes = functionNode.getAllNodes()
    for node in allNodes:
        if node.id not in visited:
            visited, stack = topologicalSortUtil(node, visited, stack, returnIDs)

    return stack


def topologicalSortUtil(node:CFG_Node, visited:dict, stack:list, returnIDs = True):
    visited[node.id] = True

    nextNodesCopy = node.nextNodes.copy()
    nextNodesCopy.reverse()
    for nextNode in nextNodesCopy:
        if nextNode.id not in visited:
            visited, stack = topologicalSortUtil(nextNode, visited, stack, returnIDs)

    if(returnIDs):
        stack.insert(0, node.id)
    else:
        stack.insert(0, node)
    return visited, stack


# converts a CFG_Node into SSA LLVM code (phi nodes incomplete)
def addNodeLabelsAndBranches(lastRegUsed, node:CFG_Node, top_env, types, functions) -> Tuple[int]:
    match node.label:
        case 'statement block node':
            if not node.visited:
                node.llvmCode.insert(0, f'l{node.id}:')
                node.visited = True
                if len(node.nextNodes) > 0 and node.nextNodes[0].id != 0:
                    node.llvmCode.append(f'br label %l{node.nextNodes[0].id}')
                return lastRegUsed
        case 'while guard node':
            if not node.visited:
                node.visited = True
                node.llvmCode.insert(0, f'l{node.id}:')
                lastRegUsed, exprVal, exprType = expressionToSSA(lastRegUsed, node.guardExpression, top_env, types, functions, node)

                whileBody = node.nextNodes[0]
                whileExit = node.nextNodes[1]

                node.llvmCode.append(f'br i1 {exprVal}, label %l{whileBody.id}, label %l{whileExit.id}')
                return lastRegUsed
        case 'if guard node':
            if not node.visited:
                node.visited = True
                node.llvmCode.insert(0, f'l{node.id}:')

                lastRegUsed, exprVal, exprType = expressionToSSA(lastRegUsed, node.guardExpression, top_env, types, functions, node)

                # every if gard node will have only 2 nodes after it
                # the node at index 0 will always be the body node
                # the node at index 1 will always be the else/exit node
                ifBlock = node.nextNodes[0]
                elseBlock = node.nextNodes[1]

                node.llvmCode.append(f'br i1 {exprVal}, label %l{ifBlock.id}, label %l{elseBlock.id}')
                return lastRegUsed
        case 'return node':
            if not node.visited:
                node.visited = True
                return lastRegUsed
        case 'if exit node' | 'while exit node':
            if not node.visited:
                node.llvmCode.insert(0, f'l{node.id}:')
                node.visited = True
                if node.nextNodes[0].id != 0:
                    node.llvmCode.append(f'br label %l{node.nextNodes[0].id}')
                return lastRegUsed


def getLLVMType(typeID:str) -> str:
    if typeID == 'bool':
        return 'i1'
    elif typeID == 'int':
        return 'i32'
    elif typeID == 'void':
        return 'void'
    else:
        return f'%struct.{typeID}*'