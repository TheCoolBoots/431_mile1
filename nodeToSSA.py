from ast_class_definitions import *
from ssaGenerator import statementToSSA


# generates initial mappings and phi nodes
def firstCFGPass(functionNode:Function_CFG):
    nodeReferences = {}
    queue = []
    queue.append(functionNode.rootNode)
    lastRegUsed = 0
    while queue != []:
        currNode = queue.pop(0)
        if currNode.id in nodeReferences:
            continue
        else:
            nodeReferences[currNode.id] = currNode
            lastRegUsed = cfgNodeToSSA(lastRegUsed)
        for node in currNode.nextNodes:
            queue.append(node)


# generates ssa code for statements inside a single cfg node
# returns the last register used
def cfgNodeToSSA(lastRegUsed:int, node:CFG_Node, top_env, types, functions) -> int:
    llvmCode = []
    for statement in node.ast_statements:
        lastRegUsed, newCode = statementToSSA(lastRegUsed, node, top_env, types, functions)
        llvmCode.extend(newCode)
    node.llvmCode = llvmCode
    return lastRegUsed