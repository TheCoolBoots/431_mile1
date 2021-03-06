from ast_class_definitions import *
from typing import Tuple

# returns list of control flow graphs
def generateProgCFGs(prog:m_prog) -> list[Function_CFG]:
    graphs = []
    for fun in prog.functions:
        returnNode = CFG_Node(0, 'return node')
        lastIDUsed = -1
        lastIDUsed, entryNode, exitNode, funReturnNode = generateStatementsCFG(lastIDUsed, fun.statements, returnNode)
        graphs.append(Function_CFG(entryNode, exitNode, returnNode, fun))
    return graphs


# returns a cfg with a single entry and exit node built from a list of statements
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateStatementsCFG(lastNodeIDUsed:int, statements:list, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    entryNode = CFG_Node(lastNodeIDUsed + 1, 'statement block node')
    lastNodeIDUsed += 1

    prevNode = entryNode
    currentStatements = []

    for i, statement in enumerate(statements):
        match statement:
            case m_conditional():
                prevNode.extendStatements(currentStatements)
                currentStatements = []

                lastNodeIDUsed, condEntry, exitNode, ifRetNode = generateIfCFG(lastNodeIDUsed, statement, returnNode)
                prevNode.addNextNode(condEntry)
                condEntry.addPrevNode(prevNode)

                prevNode = exitNode
                
                # m_cond statement returns in all branches
                if ifRetNode != None and exitNode == None:
                    if i < len(statements) - 1:
                        print(f"WARNING: unreachable code from lines {statements[i+1].lineNum} to {statements[-1].lineNum}") 
                    return lastNodeIDUsed, entryNode, None, returnNode
                else:
                    pass

            case m_loop():
                prevNode.extendStatements(currentStatements)
                currentStatements = []
                lastNodeIDUsed, condEntry, exitNode, loopRetNode = generateLoopCFG(lastNodeIDUsed, statement, returnNode)
                prevNode.addNextNode(condEntry)
                condEntry.addPrevNode(prevNode)

                prevNode = exitNode

            case m_ret():
                currentStatements.append(statement)
                prevNode.extendStatements(currentStatements)
                currentStatements = []
                prevNode.addNextNode(returnNode)
                returnNode.addPrevNode(prevNode)

                if i < len(statements) - 1:
                    print(f"WARNING: unreachable code from lines {statements[i+1].lineNum} to {statements[-1].lineNum}") 

                return lastNodeIDUsed, entryNode, None, returnNode
            case other:
                currentStatements.append(statement)

    prevNode.extendStatements(currentStatements)
    currentStatements = []
    return lastNodeIDUsed, entryNode, prevNode, None


# returns a cfg with a single entry and (exit node or return node) built from a conditional
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateIfCFG(lastNodeIDUsed:int, cond:m_conditional, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    guardNode = CFG_Node(lastNodeIDUsed+1, 'if guard node', guardExpression=cond.guard_expression)
    lastNodeIDUsed += 1
    exitNode = CFG_Node(-1, 'if exit node')

    lastNodeIDUsed, ifBlockEntry, ifBlockExit, ifReturnNode = generateStatementsCFG(lastNodeIDUsed, cond.if_statements, returnNode)
    ifBlockEntry.addPrevNode(guardNode)
    guardNode.addNextNode(ifBlockEntry)

    elseReturnNode = -1
    if cond.else_statements != [None]:
        lastNodeIDUsed, elseBlockEntry, elseBlockExit, elseReturnNode = generateStatementsCFG(lastNodeIDUsed, cond.else_statements, returnNode)
        elseBlockEntry.addPrevNode(guardNode)
        guardNode.addNextNode(elseBlockEntry)

    exitNode.id = lastNodeIDUsed + 1
    lastNodeIDUsed += 1

    # both branches exist and don't return
    if ifReturnNode == None and elseReturnNode == None:
        exitNode.addPrevNode(ifBlockExit)
        exitNode.addPrevNode(elseBlockExit)
        ifBlockExit.addNextNode(exitNode)
        elseBlockExit.addNextNode(exitNode)
        return lastNodeIDUsed, guardNode, exitNode, None
    # else branch doesnt exist and if branch doesnt return
    elif cond.else_statements == [None] and ifReturnNode == None:
        guardNode.addNextNode(exitNode)
        ifBlockExit.addNextNode(exitNode)
        exitNode.addPrevNode(guardNode)
        exitNode.addPrevNode(ifBlockExit)
        return lastNodeIDUsed, guardNode, exitNode, None
    # else branch doesnt exist and if branch returns
    elif cond.else_statements == [None] and ifReturnNode != None:
        guardNode.addNextNode(exitNode)
        exitNode.addPrevNode(guardNode)
        return lastNodeIDUsed, guardNode, exitNode, ifReturnNode
    else:
        # both branches of the if statement return
        ifReturnNode = elseReturnNode
        return lastNodeIDUsed, guardNode, None, ifReturnNode


# returns a cfg with a single entry and exit node built from a loop
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateLoopCFG(lastNodeIDUsed:int, loop:m_loop, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    guardNode = CFG_Node(lastNodeIDUsed+1, 'while guard node', guardExpression=loop.guard_expression)
    lastNodeIDUsed += 1
    exitNode = CFG_Node(-1, 'while exit node')

    lastNodeIDUsed, whileEntry, whileExit, whileReturnNode = generateStatementsCFG(lastNodeIDUsed, loop.body_statements, returnNode)
    guardNode.addNextNode(whileEntry)
    guardNode.addNextNode(exitNode)
    exitNode.addPrevNode(guardNode)
    whileEntry.addPrevNode(guardNode)

    exitNode.id = lastNodeIDUsed + 1
    lastNodeIDUsed += 1

    if whileReturnNode != None and whileExit == None:
        # while body will always return
        return lastNodeIDUsed, guardNode, exitNode, returnNode
    else:
        whileExit.addNextNode(guardNode)
        guardNode.addPrevNode(whileExit)
        guardNode.sealed = False
        return lastNodeIDUsed, guardNode, exitNode, None
    
