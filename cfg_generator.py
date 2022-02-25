from ast_class_definitions import *

class CFG_Node():
    None

class CFG_Node():
    def __init__(self, id:int, statements:list = [], sealed:bool = True, guardExpression = None) -> None:
        self.id = id
        self.ast_statements = statements
        self.guardExpression = None
        self.prevNodes = []
        self.nextNodes = []
        self.sealed = sealed

    def addPrevNode(self, node:CFG_Node):
        self.prevNodes.append(CFG_Node)

    def addNextNode(self, node:CFG_Node):
        self.prevNodes.append(CFG_Node)

    def extendStatements(self, statements:list):
        self.ast_statements.extend(statements)

class Function_CFG():
    def __init__(self, rootNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node, ast:m_function):
        self.rootNode = rootNode
        self.exitNode = exitNode
        self.returnNode = returnNode

    def serialize(self):
        pass


# returns list of control flow graphs
def generateProgCFGs(prog:m_prog) -> list(Function_CFG):
    graphs = []
    for fun in prog.functions:
        returnNode = CFG_Node(0)
        lastIDUsed = 0
        entryNode, exitNode, funReturnNode = generateStatementsCFG(fun.statements, returnNode)
        graphs.append(Function_CFG(entryNode, exitNode, returnNode, fun))
    return graphs



# returns a cfg with a single entry and exit node built from a list of statements
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateStatementsCFG(lastIDUsed:int, statements:list, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    entryNode = CFG_Node(lastIDUsed + 1)
    lastIDUsed += 1

    prevNode = entryNode
    currentStatements = []

    for i, statement in enumerate(statements):
        match statement:
            case m_conditional():
                newNode = CFG_Node(lastIDUsed+1, currentStatements)
                lastIDUsed += 1

                newNode.addPrevNode(prevNode)
                prevNode.addNextNode(newNode)

                lastIDUsed, condEntry, exitNode, ifRetNode = generateIfCFG(lastIDUsed, statement, returnNode)
                newNode.addNextNode(condEntry)
                condEntry.addPrevNode(newNode)

                prevNode = exitNode
                
                # m_cond statement returns in all branches
                if returnNode != None and exitNode == None:
                    if i < len(statements) - 1:
                        print(f"WARNING: unreachable code from lines {statements[i+1].lineNum} to {statements[-1].lineNum}") 
                    return lastIDUsed, entryNode, None, returnNode

            case m_loop():
                newNode = CFG_Node(lastIDUsed+1, currentStatements)
                lastIDUsed += 1

                newNode.addPrevNode(prevNode)
                prevNode.addNextNode(newNode)

                lastIDUsed, condEntry, exitNode, loopRetNode = generateLoopCFG(lastIDUsed, statement, returnNode)
                newNode.addNextNode(condEntry)
                condEntry.addPrevNode(newNode)

                prevNode = exitNode

            case m_ret():
                currentStatements.append(statement)
                newNode = CFG_Node(lastIDUsed+1, currentStatements)
                lastIDUsed += 1

                newNode.addPrevNode(prevNode)
                prevNode.addNextNode(newNode)
                newNode.addNextNode(returnNode)
                returnNode.addPrevNode(newNode)

                if i < len(statements) - 1:
                    print(f"WARNING: unreachable code from lines {statements[i+1].lineNum} to {statements[-1].lineNum}") 

                return lastIDUsed, entryNode, None, returnNode
            case other:
                currentStatements.append(statement)

    return lastIDUsed, entryNode, prevNode, None

    


# returns a cfg with a single entry and (exit node or return node) built from a conditional
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateIfCFG(lastIDUsed:int, cond:m_conditional, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    guardNode = CFG_Node(lastIDUsed+1, guardExpression=cond.guard_expression)
    lastIDUsed += 1
    exitNode = CFG_Node(-1)

    lastIDUsed, ifBlockEntry, ifBlockExit, ifReturnNode = generateStatementsCFG(lastIDUsed, cond.if_statements, returnNode)
    ifBlockEntry.addPrevNode(guardNode)
    guardNode.addNextNode(ifBlockEntry)

    elseReturnNode = -1
    if cond.else_statements != [None]:
        lastIDUsed, elseBlockEntry, elseBlockExit, elseReturnNode = generateStatementsCFG(lastIDUsed, cond.if_statements, returnNode)
        elseBlockEntry.addPrevNode(guardNode)
        guardNode.addNextNode(elseBlockEntry)

    exitNode.id = lastIDUsed + 1
    lastIDUsed += 1

    # both branches exist and don't return
    if ifReturnNode == None and elseReturnNode == None:
        exitNode.addPrevNode(ifBlockExit)
        exitNode.addPrevNode(elseBlockExit)
        ifBlockExit.addNextNode(exitNode)
        elseBlockExit.addNextNode(exitNode)
        return lastIDUsed, guardNode, exitNode, None
    # else branch doesnt exist and if branch doesnt return
    elif cond.else_statements == [None] and ifReturnNode == None:
        guardNode.addNextNode(exitNode)
        ifBlockExit.addNextNode(exitNode)
        exitNode.addPrevNode(guardNode)
        exitNode.addPrevNode(ifBlockExit)
        return lastIDUsed, guardNode, exitNode, None
    # else branch doesnt exist and if branch returns
    elif cond.else_statements == [None] and ifReturnNode != None:
        guardNode.addNextNode(exitNode)
        exitNode.addPrevNode(guardNode)
        return lastIDUsed, guardNode, exitNode, ifReturnNode
    else:
        # both branches of the if statement return
        ifReturnNode = elseReturnNode
        return lastIDUsed, guardNode, None, ifReturnNode



# returns a cfg with a single entry and exit node built from a loop
# returns (lastIDUsed:int, entryNode:CFG_Node, exitNode:CFG_Node, returnNode:CFG_Node)
def generateLoopCFG(lastIDUsed:int, loop:m_loop, returnNode:CFG_Node) -> Tuple[int, CFG_Node, CFG_Node, CFG_Node]:
    guardNode = CFG_Node(lastIDUsed+1, guardExpression=loop.guard_expression)
    lastIDUsed += 1
    exitNode = CFG_Node(-1)

    lastIDUsed, whileEntry, whileExit, whileReturnNode = generateStatementsCFG(lastIDUsed, loop.body_statements, returnNode)
    guardNode.addNextNode(whileEntry)
    guardNode.addNextNode(exitNode)
    exitNode.addPrevNode(guardNode)
    whileEntry.addPrevNode(guardNode)

    exitNode.id = lastIDUsed + 1
    lastIDUsed += 1

    if whileReturnNode != None and whileExit == None:
        # while body will always return
        return guardNode, exitNode, returnNode
    else:
        whileExit.addNextNode(guardNode)
        guardNode.addPrevNode(whileExit)
        guardNode.sealed = False
        return guardNode, exitNode, None
    
