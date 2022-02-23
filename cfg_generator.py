import unittest
from ast_class_definitions import *
import test_ast_trees
from enum import Enum

functionBlocks = {}  # A dict to track function names to their FunctionNodes
blockId = 0  # This will help with numbering CFG_Nodes
ifOrWhileFlag = 0  # This will tell a function if you are currently in an if or while guard


class CFG_Node:
    None


# 0 is normal, 1 is if-guard, 2 is if-convergence, 3 is while-guard, 4 is while-body
class IdCodes(Enum):
    IF_GUARD = 1        # IdCodes.IF_GUARD
    IF_CONVERGENCE = 2  # IdCodes.IF_CONVERGENCE
    WHILE_GUARD = 3     # IdCodes.WHILE_GUARD
    WHILE_BODY = 4      # IdCodes.WHILE_BODY


class CFG_Node:
    # def __init__(self, nextBlocks:list, code:list[m_statement], id:int, returnType = None): 
    def __init__(self, lastRegUsed: int, previousBlocks: list[CFG_Node], nextBlocks: list[CFG_Node], code: list,
                 id: int, idCode: list = None, returnType=None):
        self.previousBlocks = previousBlocks  # can be multiple
        self.nextBlocks = nextBlocks  # could be multiple
        self.code = code  # is a list of statements
        self.id = id
        self.returnType = returnType  # default is currently None, might wanna do m_type("void") instead, also should probably add a type
        self.mappings = {}
        self.sealed = True
        self.lastRegUsed = lastRegUsed
        self.idCode = idCode  # 0 is normal, 1 is if-guard, 2 is if-convergence, 3 is while-guard, 4 is while-body


class Function_Nodes:
    def __init__(self, firstNode: CFG_Node, lastNodes: list[CFG_Node], returnType=None,
                 ssaCode=None):  # is return type necessary
        self.firstNode = firstNode
        self.lastNodes = lastNodes
        self.returnType = returnType
        self.ssaCode = ssaCode


# returns a list of all function linked blocks. Previously it only returned the main function.
def generate_CFG_Prog_Handler(program: m_prog):
    global blockId

    functionList = []  # This will hold all of the function nodes

    # look through the functions and make them into blocks (in order)
    for fun in program.functions:
        # if you get to main, break, we deal with it specially because main should always be last
        # NOTE: dont necessarily need to do this
        if fun.id.identifier == "main":
            mainFun = fun
            break

        # create block for each function
        newNode = generate_CFG_Function_Handler(fun.statements, 0)

        # add the new block to the environment
        functionBlocks[fun.id.identifier] = newNode

        # add the block to the funciton list
        functionList.append(newNode)

    # create the main function node
    mainNode = generate_CFG_Function_Handler(mainFun.statements, 0)

    # add main to the list of functions
    functionList.append(mainNode)

    # Now we step through each function node and remove empty nodes and then renumber the CFG_Nodes
    for node in functionList:

        # START OF EMPTY NODE REMOVAL SECTION

        queue = []  # queue to keep track of which nodes we need to visit
        nodeReferences = {}  # dict to track which nodes we've visited
        queue.append(node.firstNode)  # enqueue the node at the front

        # step through the nodes and delete the empty nodes by patching the others together
        firstFlag = 1
        while queue != []:
            # grab the first node
            currNode = queue.pop(0)

            # if the node has been seen, just continue to the next
            if currNode in nodeReferences:
                continue
            else:
                nodeReferences[currNode] = True

            # if current node is none, we assume we are at the first node, and continue
            if currNode.code == [] and firstFlag == 1:
                firstFlag = 0

                # change the front node
                node.firstNode = currNode.nextBlocks[0]

                # add the new front node to the queue
                queue.append(currNode.nextBlocks[0])

                # just continue
                continue

            # check if any of the next nodes are empty
            i = 0
            while i < len(currNode.nextBlocks):
                if currNode.nextBlocks[i].code == [] and currNode.nextBlocks[i].idCode == []:

                    # add the nextBlocks of that node to the current one
                    for tempNode in currNode.nextBlocks[i].nextBlocks:
                        currNode.nextBlocks.append(tempNode)

                    # remove the node
                    currNode.nextBlocks.pop(i)

                    # continue, don't increment i as it is now removed
                    firstFlag = 0
                    continue

                # otherwise increment i
                i += 1

            # no longer at the first node
            firstFlag = 0

            # add all the next nodes to the queue
            for nextNode in currNode.nextBlocks:
                queue.append(nextNode)

        # END OF EMPTY NODE REMOVAL SECTION

        # START OF LOGICAL RENUMBERING SECTION

        # Step thru the nodes in order and renumber them in a more logical manner
        queue = []  # queue to keep track of nodes we need to visit
        nodeReferences = {}  # tracks which nodes have been visited
        queue.append(node.firstNode)  # enqueue the node at the front
        updateId = 0  # number to update with

        # step through the nodes and renumber each node in logical order
        while queue != []:
            currNode = queue.pop(0)

            # if the node is in the dict, ignore it, otherwise we add it to the dict.
            if currNode in nodeReferences:
                continue
            else:
                nodeReferences[currNode] = True

            # update the currNode id value
            currNode.id = updateId

            # increment new id value
            updateId += 1

            # add all the next nodes to the queue
            for tempNode in currNode.nextBlocks:
                queue.append(tempNode)

        # END OF LOGICAL RENUMBERING SECTION

    return functionList


# the function flag tells us if we should create a function node or just a node (0 means function, 1 means not function)
# handle each function uniquely, step through statements and create/connect nodes as needed
def generate_CFG_Function_Handler(currStatements: list, functionFlag: int):
    global blockId
    currNode = CFG_Node(-1, [], [], [], blockId)  # Something special that should go into the last used register field?
    blockId += 1  # Keep a blockId so that we can number them as we go
    currFinalBlocks = []  # We keep the final blocks so that we can put it into the function node
    initialNode = currNode  # We will keep the initial node so that we know what to return
    initialFlag = 0  # This flag will be 0 while we are still on the first node
    currNodeCount = 0  # This tracks how many nodes are in the current block

    # If we want to return a Function_Nodes struct, we must create it here.
    if functionFlag == 0:
        functionNode = Function_Nodes(None, [], None)

    # run this node through the statements until we need a new one
    for statement in currStatements:
        # add to curr node based on current statement
        # if it is an if or while, we will be adding more nodes to the currNode
        # NOTE: if we look at an if else/while statement, we return the guard node so that we can connect the nodes
        currTuple = generate_CFG_Nodes(statement, currNode)

        # save the previous node in case its been replaced (if or while)
        tempNode = currNode

        # this is the node we just generated from he statement
        currNode = currTuple[0]

        # check if we need a new node (if or while)
        if (currTuple[1] == 2 or currTuple[1] == 3):
            # if you currently have a node that is not empty ...
            if currNodeCount > 0:
                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = tempNode

            # keeps track of how many nodes there are, we need this to see when we pass the initial node
            currNodeCount = 0  # I DONT THINK THIS LINE SHOULD BE HERE, DOUBLE CHECK ME THO
            newNode = CFG_Node(-1, [], [], [], blockId)
            blockId += 1

            # m_loop
            # while statement, connect the returned guard node to the new node
            if (currTuple[1] == 2):

                # tempNode is the previous node, do we really need this?
                if (tempNode != None):
                    tempNode.nextBlocks.append(currNode)

                # simply put the newNode as a nextBlock from currNode
                currNode.nextBlocks.append(newNode)

                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # update currNode to be the newNode
                currNode = newNode

                # set the current final block to the guard statement
                currFinalBlocks = [currNode]  # THIS MAY NOT BE THE CORRECT INTERPRETATION. Dont think this even matters


            # m_conditional
            # if else statement, connect each existing next from the guard block to the new node
            elif (currTuple[1] == 3):
                # if you are on the first node, set it as the initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # get the if node
                ifNode = currNode.nextBlocks[0]

                queue = [ifNode]  # make a queue of nodes to visit
                visitedDict = {}  # keep track of visited nodes (dict)
                currFinalBlocks = []  # we will remake final blocks. Honestly, probably dont even need this.

                # search the queue while it isnt empty
                while (queue != []):
                    # pop the front
                    curr = queue.pop(0)

                    if curr in visitedDict:
                        continue
                    else:
                        visitedDict[curr] = True

                    # once you hit a node with no next nodes in its list, add the new node
                    # this adds the newNode to the if and else blocks nextBlocks lists
                    if (curr.nextBlocks == []):
                        curr.nextBlocks.append(newNode)
                        currFinalBlocks.append(curr)

                    # if a node has more nodes in its list, add them to the queue and continue
                    else:
                        for node in curr.nextBlocks:
                            queue.append(node)

                # # if the currFinalBlocks actually matters, you will need to think through this line
                # currFinalBlocks = [ifNode]

                # do all the same for the else node if it exists
                if len(currNode.nextBlocks) > 1:
                    # get the else node from the currNode
                    elseNode = currNode.nextBlocks[1]

                    queue = [elseNode]  # make a queue of nodes to visit
                    visitedDict = {}  # keep track of visited nodes (dict)
                    currFinalBlocks = []  # we will remake final blocks

                    # search the queue while it isnt empty
                    while (queue != []):
                        # pop the front
                        curr = queue.pop(0)

                        if curr in visitedDict:
                            continue
                        else:
                            visitedDict[curr] = True

                        # once you hit a node with no next nodes in its list, add the new node
                        if (curr.nextBlocks == []):
                            curr.nextBlocks.append(newNode)
                            currFinalBlocks.append(curr)
                        # if a node has more nodes in its list, add them to the queue and continue
                        else:
                            for node in curr.nextBlocks:
                                queue.append(node)

                # this will add a connection from the guard to the next node if the else doesn't exist
                else:
                    currNode.nextBlocks.append(newNode)

                # update currNode to be newNode
                if newNode.idCode is None:
                    newNode.idCode = [IdCodes.IF_CONVERGENCE]
                else:
                    newNode.idCode.append(IdCodes.IF_CONVERGENCE)  # THIS IS THE CODE FOR AN IF CONVERGENCE BLOCK

                # update the currNode to be the newNode
                currNode = newNode


        # reached return in main block
        elif (currTuple[1] == 1):
            # if you are on the first node, set it as the initial node
            if initialFlag == 0:
                initialFlag = 1
                initialNode = currTuple[0]

            # the current final block is currTuple[0]
            currFinalBlocks = [currTuple[0]]

            # break from the function, no need to go further when you hit a return
            break


        else:
            # if you are on the first node, set it as the initial node
            if initialFlag == 0:
                initialFlag = 1
                initialNode = currNode

            # I DONT THINK IS THE RIGHT THING TO DO TBH
            while currNode.nextBlocks != []:
                currNode = currNode.nextBlocks[0]
            currNodeCount += 1
    # I DONT THINK IS THE RIGHT THING TO DO TBH

    # if this is our first node, set it to initial node
    if initialFlag == 0:
        initialNode = currNode

    # Here we return the function node since functionFlag is 0.
    if functionFlag == 0:
        functionNode.firstNode = initialNode
        functionNode.lastNodes = currFinalBlocks
        return functionNode

        # You've reached the end of the function, return the intial node.
    # This is the case where functionFlag == 1.
    # We just return a CFG_Node rather than a function node.
    return initialNode


# returns a tuple that is (node, int):
# 1 if it is a return statement
# 2 if it is a while statement
# 3 if it is an if/if else statement
# return 0 if it is none of the above
def generate_CFG_Nodes(expression, currNode):
    global blockId
    global ifOrWhileFlag

    # match the expression to find out what struct it is
    match expression:
        case m_conditional():
            # call generete_CFG_Nodes on the guard statement, set this to next from the current node
            ifOrWhileFlag = 1
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1)

            # here we add the idCode for an if guard node
            if guardNode.idCode is None:
                guardNode.idCode = [IdCodes.IF_GUARD]
            else:
                guardNode.idCode.append(IdCodes.IF_GUARD)  # THIS IS THE CODE FOR AN IF GUARD BLOCK
            ifOrWhileFlag = 0

            # create a node for the if statements
            ifNode = generate_CFG_Function_Handler(expression.if_statements, 1)

            # add the if statements to the guard next block
            guardNode.nextBlocks.append(ifNode)

            # check if there is an else
            if expression.else_statements != [None]:
                # create a node for the else statements
                elseNode = generate_CFG_Function_Handler(expression.else_statements, 1)

                # this else node is added as a next block to the if guard
                guardNode.nextBlocks.append(elseNode)

            # currNode adds guardNode as its next block
            currNode.nextBlocks.append(guardNode)

            # here we return 3 to indicate that this was an m_conditional
            return (guardNode, 3)

        case m_loop():
            # call generete_CFG_Nodes on the guard statement, set this to next from the current node
            ifOrWhileFlag = 1
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1)

            # here we add the idCode for a guardNode
            if guardNode.idCode is None:
                guardNode.idCode = [IdCodes.WHILE_GUARD]
            else:
                guardNode.idCode.append(IdCodes.WHILE_GUARD)  # THIS IS THE CODE FOR A WHILE GUARD BLOCK
            ifOrWhileFlag = 0

            # call generete_CFG_Nodes on the statement in the while, this generates the whileNode for us
            whileNode = generate_CFG_Function_Handler(expression.body_statements, 1)

            # here we add the idCode for a while body node
            if whileNode.idCode is None:
                whileNode.idCode = [IdCodes.WHILE_BODY]
            else:
                whileNode.idCode.append(IdCodes.WHILE_BODY)  # THIS IS THE CODE FOR A WHILE BODY BLOCK

            # set this to next from the guard node, next from this should also be the guard node
            guardNode.nextBlocks.append(whileNode)

            # make a queue of nodes to visit
            queue = [whileNode]

            # keep track of visited nodes (dict)
            visitedDict = {}

            # search the queue while it isnt empty
            while (queue != []):
                # pop the front
                curr = queue.pop(0)

                if curr in visitedDict:
                    continue

                else:
                    visitedDict[curr] = True

                # once you hit a node with no next nodes in its list, add the new node
                if (curr.nextBlocks == []):
                    curr.nextBlocks.append(guardNode)

                # if a node has more nodes in its list, add them to the queue and continue
                else:
                    for node in curr.nextBlocks:
                        queue.append(node)

            # here we return 2 to indicate that this was an m_loop
            return (guardNode, 2)

        case m_ret():
            # If we wanted to set the return type of the current node, this might be a good place to do it
            currNode.code.append(expression)

            temp = checkForInvocation(expression.expression, currNode)
            currNode = temp[2]

            # Previously, this block patched in the invocation node (when I was doing that)
            # # if there was an invocation, add the node to your current node
            # if temp[1] == 1:
            #     newNode = temp[0]
            #
            #     # make sure you find the end of currNode before continuing
            #     while currNode.nextBlocks != []:
            #         currNode = currNode.nextBlocks[0]
            #
            #     # now patch in the new invocation node
            #     currNode.nextBlocks.append(newNode)
            #     # make the current node the new one
            #     currNode = newNode

            # here we return 1 to indicate that this was an m_ret
            return (currNode, 1)

        case m_print():
            currNode.code.append(expression)

            temp = checkForInvocation(expression.expression, currNode)
            currNode = temp[2]

            # Previously, this block patched in the invocation node (when I was doing that)
            # # if there was an invocation, add the node to your current node
            # if temp[1] == 1:
            #     # print("ENTERED ARG INVOCATION BLOCK")
            #     newNode = temp[0]
            #     # print("found a new invocation: " + str(newNode))
            #
            #     # make sure you find the end of currNode before continuing
            #     while currNode.nextBlocks != []:
            #         currNode = currNode.nextBlocks[0]
            #
            #     # now patch in the new invocation node
            #     currNode.nextBlocks.append(newNode)
            #     # make the current node the new one
            #     currNode = newNode

            # here we return 0 to indicate that this was not a return, loop, or conditional
            return (currNode, 0)

        case m_assignment():
            # add the assignment code to the node
            currNode.code.append(expression)

            # check for invocation inside the sub expression (it would need to be added to code)
            newTuple = checkForInvocation(expression.source_expression, currNode)
            currNode = newTuple[2]

            # here we return 0 to indicate that this was not a return, loop, or conditional
            return (currNode, 0)

        # this case will catch the rest of the possible expressions
        case _:
            # this flag indicates that we are in a guard node - the only time when we should be appending these expressions
            # this should only be m_bool, unary, binop
            if (ifOrWhileFlag == 1):
                currNode.code.append(expression)

            # here we return 0 to indicate that this was not a return, loop, or conditional
            return (currNode, 0)


# this function is used to check sub expressions.
# It works very nice for seeing when you have nested invocations, you need to add these to the code field of currNode.
def checkForInvocation(expression, currNode):
    global blockId

    # check what structure you have in  the expression
    match expression:

        case m_invocation():
            # add the invocation expression to the currNode code
            currNode.code.append(expression)

            # step through each argument in the invocation
            # this loop only matters when you have a nested invocation, it should be added to the code if it is there
            for exp in expression.args_expressions:
                currTuple = checkForInvocation(exp, currNode)
                currNode = currTuple[2]

            return (None, 1, currNode)

        # these expressions should never be appended to the code
        case m_num() | m_new_struct() | m_null() | m_dot() | m_id():
            return (None, 0, currNode)

        # this case is used for catching stuff that might be in the guard statement and appending the code
        case m_bool() | m_binop() | m_unary():
            # this flag indicates that we are in a guard node - the only time when we should be appending these expressions
            if ifOrWhileFlag == 1:
                currNode.code.append(expression)
            return (None, 0, currNode)

        # in case I missed any expressions (there are several I would miss intentionally)
        case _:
            return (None, 0, currNode)
