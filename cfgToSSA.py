from pyclbr import Function
from re import L
from ssaGenerator import expressionToSSA, generateSSA, readUnsealedBlock, statementToSSA
from cfg_generator import generateProgCFGs
from ast_class_definitions import *
from ssaGenerator import readVariable


# converts an m_prog into an SSA LLVM program
def topSSACompile(prog:m_prog) -> list[str]:
    functionNodes = generateProgCFGs(prog)
    types = prog.getTopTypeEnv()
    typeSizes = prog.getTypeSizes()
    functions = {}

    typeDefs = [typeDef.getLLVM() for typeDef in prog.types]
    globalDeclarations = [globalDec.getSSAGlobals() for globalDec in prog.global_declarations]

    code = typeDefs
    code.extend(globalDeclarations)

    for fnode in functionNodes:
        functionCode = []

        functionDef = fnode.ast
        top_env = prog.getTopEnv(False)

        params = []
        paramTypes = []
        for param in functionDef.param_declarations:
            paramTypes.append(param.type)
            params.append(f'{getLLVMType(param.type.typeID)} %{param.id.identifier}')
            top_env[param.id.identifier] = param.type
            params = ', '.join(params)
        if len(params) == 0:
            params = ''
    
        functionCode.append(f'define {getLLVMType(functionDef.return_type.typeID)} @{functionDef.id.identifier}({params})' + ' {')
        if functionDef.id.identifier == 'main':
            functionCode.append('entry:')

        for declaration in functionDef.body_declarations:
            if declaration.type.typeID != 'int' and declaration.type.typeID != 'bool' and declaration.type.typeID != 'null':
                top_env[declaration.id.identifier] = declaration.type
                functionCode.append(declaration.getSSALocals(typeSizes))

        functions[functionDef.id.identifier] = (functionDef.return_type, paramTypes)

        # register 0 will be reserved for the return value
        lastRegUsed, bodyCode, exitNode = cfgToSSA(0, fnode.rootNode, top_env, types, functions)
        functionCode.extend(bodyCode)
        functionCode.append(f'retLabel:')
        functionCode.append(f'ret {getLLVMType(functionDef.return_type.typeID)} %0')
        functionCode.append('}')

        functionCode = sealUnsealedBlocks(fnode, functionCode)

        phiNodeIndices = []
        for i, line in enumerate(functionCode):
            if line[-1] == ']':
                phiNodeIndices.append(i)

        functionCode = fillPhiPlaceholderLabels(functionCode, phiNodeIndices)

        code.extend(functionCode)

    return code


def sealUnsealedBlocks(functionNode:Function_CFG, functionCode:list[str]) -> list[str]:
    unsealedNodes = functionNode.getUnsealedNodes()
    if len(unsealedNodes.values()) == 0:
        return functionCode

    for i, line in enumerate(functionCode):
        if line[-1] == '*':
            parts = line.split('-')
            targetReg = int(parts[0])
            nodeID = int(parts[1])
            targetID = parts[2]
            unsealedNodes[nodeID].sealed = True
            targetReg, llvmType, newLine, lastLabel = readUnsealedBlock(targetReg-1, targetID, unsealedNodes[nodeID])
            functionCode[i] = newLine[0]
    
    return functionCode


def fillPhiPlaceholderLabels(functionCode:list[str], phiNodeIndices:list[int]) -> list[str]:
    for i in phiNodeIndices:
        # %5 = phi i32 [%9, %PLACEHOLDER], [%1, %PLACEHOLDER]
        line = functionCode[i]

        # [%9, %PLACEHOLDER], [%1, %PLACEHOLDER]
        registers = line[line.find('['):]
        registers = registers.replace(',', '')
        registers = registers.replace('[', '')
        registers = registers.replace(']', '')

        # %9 %PLACEHOLDER %1 %PLACEHOLDER
        registers = registers.split(' ')

        # %9, %1 
        src1 = registers[0]
        src2 = registers[2]
        
        for j in range(0, len(functionCode)):
            if src1 in functionCode[j] and j != i:
                start1 = j
                break
        label1 = 'entry'
        for j in range(start1, 0, -1):
            if functionCode[j][-1] == ':':
                label1 = functionCode[j][:-1]
                break

        for j in range(0, len(functionCode)):
            if src2 in functionCode[j] and j != i:
                start2 = j
                break
        label2 = 'entry'
        for j in range(start2, 0, -1):
            if functionCode[j][-1] == ':':
                label2 = functionCode[j][:-1]
                break

        newLine = line[:line.find('[')] + f'[{src1}, %{label1}], [{src2}, %{label2}]'
        functionCode[i] = newLine

    return functionCode


# converts a CFG_Node into SSA LLVM code (phi nodes incomplete)
def cfgToSSA(lastRegUsed, node:CFG_Node, top_env, types, functions) -> Tuple[int, list[str], CFG_Node]:
    match node.label:
        case 'statement block node':
            lastRegUsed, code = generateSSA(lastRegUsed, node, top_env, types, functions)
            exitNode = node
            node.visited = True
            if len(node.nextNodes) >= 1: # and not node.nextNodes[0].visited:
                lastRegUsed, subsequentCode, exitNode = cfgToSSA(lastRegUsed, node.nextNodes[0], top_env, types, functions)
                code.extend(subsequentCode)
            return lastRegUsed, code, exitNode
        case 'while guard node':
            if not node.visited:
                node.visited = True
                lastRegUsed, code, exitNode = whileNodeToSSA(lastRegUsed, node, top_env, types, functions)
                return lastRegUsed, code, exitNode
            else:
                return lastRegUsed, [], node
        case 'if guard node':
            node.visited = True
            lastRegUsed, code, exitNode = ifNodeToSSA(lastRegUsed, node, top_env, types, functions)
            if len(exitNode.nextNodes) >= 1:
                lastRegUsed, subsequentCode, exitNode = cfgToSSA(lastRegUsed, exitNode.nextNodes[0], top_env, types, functions)
                code.extend(subsequentCode)
            return lastRegUsed, code, exitNode
        case 'return node':
            lastRegUsed, code = generateSSA(lastRegUsed, node, top_env, types, functions)
            node.visited = True
            return lastRegUsed, code, node
        case 'if exit node' | 'while exit node':
            node.visited = True
            return lastRegUsed, [], node



def whileNodeToSSA(lastRegUsed, node:CFG_Node, top_env, types, functions) -> Tuple[int, list[str], CFG_Node]:
    saveReg = lastRegUsed
    lastRegUsed += 3
    outputCode = [f'{saveReg + 1}:']
    expressionReg, retType, expressionCode = expressionToSSA(lastRegUsed, node.guardExpression, top_env, types, functions, node)
    outputCode.extend(expressionCode)
    outputCode.extend([f'br i32 %{expressionReg}, label %{saveReg + 2}, label %{saveReg + 3}',
                        f'{saveReg + 2}:'])
    
    if expressionReg > lastRegUsed:
        lastRegUsed = expressionReg
    
    # every while gard node will have only 2 nodes after it
    # the node at index 0 will always be the body node
    # the node at index 1 will always be the exit node
    whileBody = node.nextNodes[0]
    whileExit = node.nextNodes[1]

    lastRegUsed, whileBodyCode, bodyExitNode = cfgToSSA(lastRegUsed, whileBody, top_env, types, functions)
    outputCode.extend(whileBodyCode)

    if bodyExitNode.label == 'return node':
        lastRegUsed, retNode, retExitNode = cfgToSSA(lastRegUsed, bodyExitNode, top_env, types, functions)
        outputCode.extend(retNode)
    else:
        outputCode.append(f'br label %{saveReg + 1}')

    outputCode.append(f'{saveReg + 3}:')

    lastRegUsed, exitNodeCode = generateSSA(lastRegUsed, whileExit, top_env, types, functions)
    outputCode.extend(exitNodeCode)

    return lastRegUsed, outputCode, whileExit


def ifNodeToSSA(lastRegUsed, node:CFG_Node, top_env, types, functions) -> Tuple[int, list[str], CFG_Node]:
    lastRegUsed, retType, outputCode = expressionToSSA(lastRegUsed, node.guardExpression, top_env, types, functions, node)
    regStore = lastRegUsed
    
    outputCode.extend([f'br i32 %{regStore}, label %{regStore + 1}, label %{regStore + 2}',
                        f'{regStore + 1}:'])

    # every if gard node will have only 2 nodes after it
    # the node at index 0 will always be the body node
    # the node at index 1 will always be the else/exit node
    ifBlock = node.nextNodes[0]
    elseBlock = node.nextNodes[1]
    if elseBlock.label == 'if exit node':
        lastRegUsed += 2
    else:
        lastRegUsed += 3

    lastRegUsed, ifBlockCode, ifBlockExitNode = cfgToSSA(lastRegUsed, ifBlock, top_env, types, functions)
    outputCode.extend(ifBlockCode)


    if ifBlockExitNode.label == 'return node':
        lastRegUsed, retNodeCode, ifBlockExitNode = cfgToSSA(lastRegUsed, ifBlockExitNode, top_env, types, functions)
        outputCode.extend(retNodeCode)

    # there exists an else block, thus need to add jump to bypass it
    if elseBlock.label != 'if exit node' and ifBlockExitNode.label != 'return node':
        outputCode.append(f'br label %{regStore + 3}')  

    # label for else block or exit label (if no else block exists)
    outputCode.append(f'{regStore + 2}:')

    elseBlockExitNode = None
    if elseBlock.label != 'if exit node':
        lastRegUsed, elseBlockCode, elseBlockExitNode = cfgToSSA(lastRegUsed, elseBlock, top_env, types, functions)
        outputCode.extend(elseBlockCode)

        if elseBlockExitNode.label == 'return node':
            lastRegUsed, returnNodeCode, elseBlockExitNode = cfgToSSA(lastRegUsed, elseBlockExitNode, top_env, types, functions)
            outputCode.extend(returnNodeCode)
        else:
            outputCode.append(f'{regStore + 3}:')

    if elseBlockExitNode == None:
        lastRegUsed, exitNodeCode = generateSSA(lastRegUsed, ifBlockExitNode, top_env, types, functions)
    else:
        lastRegUsed, exitNodeCode = generateSSA(lastRegUsed, elseBlockExitNode, top_env, types, functions)
    outputCode.extend(exitNodeCode)

    return lastRegUsed, outputCode, ifBlockExitNode


def getLLVMType(typeID:str) -> str:
    if typeID == 'bool' or typeID == 'int':
        return 'i32'
    elif typeID == 'void':
        return 'void'
    else:
        return f'%struct.{typeID}*'