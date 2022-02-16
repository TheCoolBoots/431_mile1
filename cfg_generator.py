import unittest
from ast_class_definitions import *
import test_ast_trees


functionBlocks = {} 
blockId = 0
ifOrWhileFlag = 0 # this will tell a function if you are currently in an if or while guard

class CFG_Node:
    None

class CFG_Node:
    # def __init__(self, nextBlocks:list, code:list[m_statement], id:int, returnType = None): 
    def __init__(self, lastRegUsed:int, previousBlocks:list[CFG_Node], nextBlocks:list[CFG_Node], code:list, id:int, idCode:list = None, returnType = None):
        self.previousBlocks = previousBlocks # can be multiple
        self.nextBlocks = nextBlocks # could be multiple
        self.code = code    # is a list of statements
        self.id = id
        self.returnType = returnType # default is currently None, might wanna do m_type("void") instead, also should probably add a type
        self.mappings = {}
        self.sealed = False
        self.lastRegUsed = lastRegUsed
# WEIRD BUG HERE, FOR SOME REASON idCode IS THE SAME FOR EVERY NODE IN A FUNCTION BLOCK
        self.idCode = idCode  # 0 is normal, 1 is if-guard, 2 is if-convergence, 3 is while-guard, 4 is while-body


class Function_Nodes:
    def __init__(self, firstNode:CFG_Node, lastNodes:list[CFG_Node], returnType = None): # is return type necessary
        self.firstNode = firstNode
        self.lastNodes = lastNodes
        self.returnType = returnType


# returns a list of all function linked blocks. Previously it only returned the main function.
def generate_CFG_Prog_Handler(program:m_prog):
    global blockId
    # print("entered Prog_Handler")

    functionList = []

    # look through the functions and make them into blocks (in order)
    for fun in program.functions:
        # if you get to main, break, this is a special case (??)
        if(fun.id.identifier) == "main":
            # print("\n\ncheck main")
            # print("function name: " + fun.id.identifier)
            mainFun = fun
            break
        # print("function name: " + fun.id.identifier)
        # create block for each function
        newNode = generate_CFG_Function_Handler(fun.statements, 0)

        # add the new block to the environment
        functionBlocks[fun.id.identifier] = newNode
        # add the block to the funciton list
        functionList.append(newNode)



    # once we get to main we will continue making blocks but also piecing together the other functions
    # print("LOOK HERE: " + str(mainFun.statements))
    mainNode = generate_CFG_Function_Handler(mainFun.statements, 0)
    # print(str(functionBlocks))
    # print("\n\nENTERING NODE REMOVAL\n\n")

    # print(str(type(mainNode)))

    functionList.append(mainNode)

    # print("function list a : " + str(functionList))


    for node in functionList:
        # print(str(type(node)))
        queue = []
        nodeReferences = {}
        # enqueue the node at the front
        queue.append(node.firstNode)
        updatePrevFlag = 1

        # step through the nodes and delete the empty nodes by patching the others together
        firstFlag = 1
        while queue != []:
            currNode = queue.pop(0)

            if currNode in nodeReferences:
                continue
            else:
                nodeReferences[currNode] = True

            # print("currID: " + str(currNode.id) )
            # print("currID: " + str(currNode.id) +  " Queue Size: " + str(len(queue)) + " Queue: " + str(queue))

            # if current node is none, we assume we are at the first node, and continue
            if currNode.code == [] and firstFlag == 1:
                firstFlag = 0
                # print("1 removing node number: " + str(currNode.id))

                # # the weird empty node branches into 2+
                # if len(currNode.nextBlocks) > 1:
                #     print("\n\n\n\nNO IDEA WHAT I SHOULD DO IN THIS CASE 1\n\n\n\n")
                #     return None
                #
                # # the empty node has no next blocks, I guess just return it
                # if len(currNode.nextBlocks) == 0:
                #     print("\n\n\n\nNO IDEA WHAT I SHOULD DO IN THIS CASE 2\n\n\n\n")
                #     return mainNode

                # change the front node
                mainNode.firstNode = currNode.nextBlocks[0]

                # add the new front node to the queue
                queue.append(currNode.nextBlocks[0])

                # just continue
                continue



            # check if any of the next nodes are
            i = 0
            # print("length: " + str(len(currNode.nextBlocks)))
            while i < len(currNode.nextBlocks):
                # print(currNode.nextBlocks)
                if currNode.nextBlocks[i].code == [] and currNode.nextBlocks[i].idCode == []:
                    # print("2 removing node number: " + str(currNode.nextBlocks[i].id))
                    # print("removed node nextBlocks: " + str(currNode.nextBlocks[i].nextBlocks))

                    # add the nextBlocks of that node to the current one
                    for tempNode in currNode.nextBlocks[i].nextBlocks:
                        # print("Here")
                        currNode.nextBlocks.append(tempNode)

                    # remove the node
                    currNode.nextBlocks.pop(i)
                    # continue, dont increment i as it is now removed
                    firstFlag = 0
                    continue

                i += 1

            firstFlag = 0

            # add all the next nodes to the queue
            for nextNode in currNode.nextBlocks:
                queue.append(nextNode)



        # LOGICAL RENUMBERING SECTION
        # step thru the nodes in order and renumber them in a more logical manner
        queue = []
        nodeReferences = {}

        # enqueue the node at the front
        queue.append( node.firstNode )

        # number to update with
        updateId = 0

        # step through the nodes and renumber each node in order
        while queue != []:
            currNode = queue.pop(0)

            # if the node is in the dict, ignore it. Otherwise we add it to the dict.
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


            # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.id)]) + "\nblock Id: " + str(currNode.id) + "\n\n\n")
            # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.code)]) + "\n\n\n")
            # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) +       "\n\n\n")# + "\nnumReferences: " + str(nodeReferences[nodeNum]) + "\n\n\n")



    # printCFG(functionList[len(functionList)-1])

    # print("function list b : " + str(functionList))

    # print("\n\nEXITING NODE REMOVAL\n\n")
    return functionList


# the function flag tells us if we should create a function node or just a node (0 means function, 1 means not function)
# handle each function uniquely, step through statements and create/connect nodes as needed
def generate_CFG_Function_Handler(currStatements:list, functionFlag:int):
    global blockId
    # print("entered Function_Handler with flag " + str(functionFlag))
    # create a node
    currNode = CFG_Node(-1 ,[], [], [], blockId) # NO IDEA WHAT I SHOULD PUT IN THE LAST USED REGISTER FIELD
    blockId += 1
    currFinalBlocks = []
    initialNode = currNode 
    initialFlag = 0

    if functionFlag == 0:
        functionNode = Function_Nodes(None, [], None)
    
    currNodeCount = 0
    updateFlag = 0
    # run this node through the statements until we need a new one
    # print("ALL STATEMENTS: " + str(currStatements))
    for statement in currStatements:
        # print("curr statement: " + str(statement))
        # add to curr node based on current statement
        # NOTE: if we look at an if else/while statement, we return the guard node so that we can connect the nodes
        currTuple = generate_CFG_Nodes(statement, currNode)

        # print("return val: " + str(currTuple[1]))

        # save the previous node in case its been replaced
        tempNode = currNode

        # i need to do this since python doesnt pass by reference
        currNode = currTuple[0]

        # print("\ncurr Node Id: " + str(currNode.id))
        # print("curr Node code: " + str(currNode.code))
        # print("node next nodes: " + str(currNode.nextBlocks))
        # print("return val: " + str(currTuple[1]))


        # might be a weird edge case on the last statement
        # check if we need a new node (if or while)
        if(currTuple[1] > 1 and currTuple[1] < 4):
            
            # if you currently have a node that is not empty ...
            if currNodeCount > 0:  
                # add the tempNode to the linked list before you get rid of it for good
                # tempNode.nextBlocks.append(currNode) # WAS IN  DO WE WANT THIS LINE BACK?????
                # currNode.previousBlocks.append(tempNode) # WAS IN

                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = tempNode
                
            # do we even need currNodeCount?
            currNodeCount = 0
            newNode = CFG_Node(-1, [], [], [], blockId)
            blockId += 1

            # m_loop
            # while statement, connect the returned guard node to the new node
            if(currTuple[1] == 2):
                # print("\tentered while block")

                if(tempNode != None): # this should fix that potential bug
                    tempNode.nextBlocks.append(currNode) # what if the tempNode is None?
                    # currNode.nextBlocks[0].nextBlocks.append(newNode) # this was creating an extra link

                # simply put the newNode as a nextBlock from currNode and ...
                currNode.nextBlocks.append(newNode) # WHAT IF THE NEW NODE IS NEVER FILLED IN? - it would get removed in the driver function

                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # print("currNode next blocks: " + str(currNode.nextBlocks))

                # update currNode to be newNode
                currNode = newNode

                # set the current final block to the guard statement
                currFinalBlocks = [currNode] # --> THIS MAY NOT BE THE CORRECT INTERPRETATION <--

            # m_conditional
            # if else statement, connect each existing next from the guard block to the new node
            else:
                # print("\tentered if block")
                # if you are on the first node, set it as the initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # get the if node and also the else node if it exists
                ifNode = currNode.nextBlocks[0]


                # FIRST STEP TO THE END OF THE IF BRANCH(S), AND THEN CONNECT TO THE NEW NODE
                    # new function for this? could be many recursively
                    # need to think specially about the while case since it would loop, what do we do when we see a node twice?


                # make a queue of nodes to visit
                queue = [ifNode]

                # keep track of visited nodes (dict)
                visitedDict = {}

                # we will remake final blocks
                currFinalBlocks = []

                # search the queue while it isnt empty
                while(queue != []):
                    # pop the front
                    curr = queue.pop(0)

                    if curr in visitedDict:
                        continue
                    else:
                        visitedDict[curr] = True


                    # once you hit a node with no next nodes in its list, add the new node
                    if(curr.nextBlocks == []):
                        curr.nextBlocks.append(newNode)
                        currFinalBlocks.append(curr)

                        # if a node has more nodes in its list, add them to the queue and continue
                    else:
                        for node in curr.nextBlocks:
                            queue.append(node)


                # # simply put the newNode as a nextBlock from both the if and else Nodes and ...
                # ifNode.nextBlocks.append(newNode) # THIS IS ALMOST CERTAINLY THE ISSUE



                # NEED TO REPLACE THIS WITH SOMETHING
                # # set the current final block to the if statement
                # currFinalBlocks = [ifNode]






                # do all the same for the else node if it exists
                if len(currNode.nextBlocks) > 1:
                    # print("\tit is also an else block")
                    elseNode = currNode.nextBlocks[1]



                    # elseNode.nextBlocks.append(newNode)



                    # make a queue of nodes to visit
                    queue = [elseNode]

                    # keep track of visited nodes (dict)
                    visitedDict = {}

                    # we will remake final blocks
                    currFinalBlocks = []

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


                # this will add a connection from the guard to the next node if the else doesnt exist
                else:
                    currNode.nextBlocks.append(newNode)



                    # # add the else block to current final blocks
                    # currFinalBlocks.append(elseNode)

                # update currNode to be newNode
                if newNode.idCode is None:
                    newNode.idCode = [2]
                else:
                    newNode.idCode.append(2)  # THIS IS THE CODE FOR AN IF CONVERGENCE BLOCK
                # print("adding 2 to idcode\n")

                # print("currNode nextBlocks: " + str(currNode.nextBlocks))
                currNode = newNode


        # reached function invocation error in block - probably not necessary
        elif(currTuple[1] == -1):
            # there are no valid nodes to return (make sure this is what you want)
            return None
            
        # reached return in main block
        elif(currTuple[1] == 1):
            # if you are on the first node, set it as the initial node
            if initialFlag == 0:
                initialFlag = 1
                initialNode = currTuple[0]

            # the current final block is currTuple[0]
            currFinalBlocks = [currTuple[0]]

            # break from the function, no need to go further when you hit a return
            break # this may actually be incorrect, need to double check where this function is called

        # invocation Case
        elif(currTuple[1] == 4):
            # print("GOT TO THE 4 CASE")
            # if you are on the first node, set it as the initial node
            if initialFlag == 0:
                initialFlag = 1
                initialNode = currTuple[0]

            # step to the end of the currNode linked list
            while currNode.nextBlocks != []:
                currNode = currNode.nextBlocks[0]

            # print("CURRENT NODE BEFORE: " + str(currNode))
            newNode = CFG_Node(-1, [],[],[], blockId)
            blockId += 1
            currNode.nextBlocks.append(newNode)
            # print("UMMMMMM" + str(currNode.code))

            # set the currNode
            currNode = newNode

            # print("CURRENT NODE AFTER: " + str(currNode))
            
        else:
            # if you are on the first node, set it as the initial node
            if initialFlag == 0:
                initialFlag = 1
                initialNode = currNode

            while currNode.nextBlocks != []:
                currNode = currNode.nextBlocks[0]
            currNodeCount += 1
    
    # if this is our first node, set it to initial node
    if initialFlag == 0:
        initialNode = currNode


    # here we return the function node
    if functionFlag == 0:
        # print("return 1")
        # print("initialNode: " + str(initialNode))
        functionNode.firstNode = initialNode
        functionNode.lastNodes = currFinalBlocks
        return functionNode 

    # youve reached the end of the function, return the intial node
    # print("return 2")
    return initialNode


# returns a tuple that is (node, int) - 
    # return 0 if you can just continue
    # 1 if it is a return statement
    # 4 if it is an invocation
    # 2 if it is a while statement 
    # 3 if it is an if/if else statement
def generate_CFG_Nodes(expression, currNode):
    global blockId
    global ifOrWhileFlag
    # print("entered low level CFG function")
    match expression:

        # conditional → if ( expression ) block {else block}opt
        # GUARD statement IS ITS OWN BLOCK
        case m_conditional():
            # print("\t--conditional case--")
            # print("\tif statement: " + str(expression.if_statements))
            # print("\telse statement: " + str(expression.else_statements))

            # call generete_CFG_Nodes on the guard statement, set this to next from the current node
            # DO I EVEN WANT TO EVALUATE THE GUARD EXPRESSION ?????
            ifOrWhileFlag = 1
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1)
            if guardNode.idCode is None:
                guardNode.idCode = [1]
            else:
                guardNode.idCode.append(1)  # THIS IS THE CODE FOR AN IF GUARD BLOCK
            # print("adding 1 to idcode\n")
            ifOrWhileFlag = 0

            # if you got a function environment error - probably not needed
            if(guardNode == None):
                # make sure this is what you want
                return None

            # call generete_CFG_Nodes on the new branch, set this to next from the guard node
            ifNode = generate_CFG_Function_Handler(expression.if_statements, 1)

            # error case - probably not needed
            if(ifNode == None):
                return None

            # add the if statements to the guard
            guardNode.nextBlocks.append(ifNode)

            # print("\n\n\n\n" + str(expression.else_statements) + "\n\n\n\n")
            # check if there is an else
            if expression.else_statements != [None]:
                # print("\t\tthere is in fact an else block")
                # call generate_CFG_Nodes on this new branch with its statements and also set this to next from the guard node
                elseNode = generate_CFG_Function_Handler(expression.else_statements, 1)
                if(elseNode == None):
                    return None
                guardNode.nextBlocks.append(elseNode)

            currNode.nextBlocks.append(guardNode)
            return (guardNode, 3)

        case m_loop():
            # print("loop case")

            # call generete_CFG_Nodes on the guard statement, set this to next from the current node
            # DO I EVEN WANT TO EVALUATE THE GUARD EXPRESSION ?????
            ifOrWhileFlag = 1
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1)
            # print("adding 3 to idcode\n")

            if guardNode.idCode is None:
                guardNode.idCode = [3]
            else:
                guardNode.idCode.append(3)  # THIS IS THE CODE FOR A WHILE GUARD BLOCK
            ifOrWhileFlag = 0

            if guardNode == None:
                # print("guard None")
                return None

            # call generete_CFG_Nodes on the statement in the while
            whileNode = generate_CFG_Function_Handler(expression.body_statements, 1)
            if whileNode.idCode is None:
                whileNode.idCode = [4]
            else:
                whileNode.idCode.append(4)  # THIS IS THE CODE FOR A WHILE BODY BLOCK
            # print("adding 4 to idcode\n")

            # error case (probably dont need)
            if whileNode == None:
                # print("while None")
                return None
            
            # print("WHILE NODE NEXT BLOCKS: " + str(whileNode.nextBlocks))
            # add the while statements
            # whileNode.code.append(expression.body_statements) # This should already be done

            # its next should be the while statements and also the code after it (???)
            # set this to next from the guard node, next from this should also be the guard node
            guardNode.nextBlocks.append(whileNode)
# MAY WANT TO ADD THIS LINE BACK





# # THIS IS THE PROBLEM, NEED TO TRAVERSE THE NODE TO FIND THE FINAL BLOCK
            # whileNode.nextBlocks.append(guardNode)

            # make a queue of nodes to visit
            queue = [whileNode]

            # keep track of visited nodes (dict)
            visitedDict = {}

            # search the queue while it isnt empty
            while (queue != []):
                # pop the front
                curr = queue.pop(0)

                if curr in visitedDict:
                # I DONT UNDERSTAND WHY I WOULD NEED THIS, IT SEEMS LIKE THE: if (curr.nextBlocks == []) line deals with this issue ????
                    # # if there is one thing in the nextBlocks and its in the visitedDict, append
                    # if(len(curr.nextBlocks) == 1 and curr.nextBlocks[0] in visitedDict):
                    #     curr.nextBlocks.append(guardNode)
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





            # print("guardNode next nodes: " + str(guardNode.nextBlocks))
            # print("whileNode next nodes: " + str(whileNode.nextBlocks))

            # return the guard node
            return (guardNode, 2)

        case m_ret():
            # print("return case")
            # print("REAAAAD" + str(currNode))
            # set the return type of the current node ???
            # currNode.returnType =  ... # MIGHT NEED SOME SORT OF FUNCTION TO GET THE TYPE FROM me_ret.expression
            currNode.code.append(expression)

            # currNode.code.append(expression.expression) # REMOVED THIS

            temp = checkForInvocation(expression.expression, currNode)
            currNode = temp[2]

            # if there was an invocation, add the node to your current node
            if temp[1] == 1:
                # print("ENTERED ARG INVOCATION BLOCK")
                newNode = temp[0]
                # print("found a new invocation: " + str(newNode))

                # make sure you find the end of currNode before continuing
                while currNode.nextBlocks != []:
                    currNode = currNode.nextBlocks[0]
                
                # now patch in the new invocation node
                currNode.nextBlocks.append(newNode)
                # make the current node the new one
                currNode = newNode

            return (currNode, 1)

        case m_print():
            
            currNode.code.append(expression)
            # currNode.code.append(expression.expression) # REMOVED THIS

            temp = checkForInvocation(expression.expression, currNode) 
            currNode = temp[2]

            # if there was an invocation, add the node to your current node
            if temp[1] == 1:
                # print("ENTERED ARG INVOCATION BLOCK")
                newNode = temp[0]
                # print("found a new invocation: " + str(newNode))

                # make sure you find the end of currNode before continuing
                while currNode.nextBlocks != []:
                    currNode = currNode.nextBlocks[0]
                
                # now patch in the new invocation node
                currNode.nextBlocks.append(newNode)
                # make the current node the new one
                currNode = newNode

            return (currNode, 0)

        # case m_invocation():
        #     # print("INVOCATION CASE")
        #     # print("CURR NODE: " + str(currNode))
        #     initial = currNode
        #     # print(str(expression))
        #     # print("LOOOOOOOOK" + str(expression.args_expressions))
        #     # print("GOT THRU THAT SHIT")
        #     # print(str(newNode))
        #     newFunctionNode = functionBlocks[expression.id.identifier]
        #     # print(newFunctionNode.firstNode)
        #     # print("LOOOOOOOOK" + str(expression.args_expressions))
        #     # step through the expressions and check if they have an invocation
        #     for exp in expression.args_expressions:
        #         # # this adds the code from each argument into the initial node

        #         # initial.code.append(expression) # THIS WAS INCORRECT
        #         # initial.code.append(exp) # REMOVED THIS, HIS IS WHAT I WANTED, BUT THIS WOULD BE ADDING A STATEMENT POTENTIALLY

        #         # this give us (Node/None, 0/1) - 0 means no invocation, 1 means invocation
        #         temp = checkForInvocation(exp, initial) 
        #         initial = temp[2]
        # # IF I WANTED TO ADD NESTED CODE (example: binop sub expressions) FROM THE INVOCATION CHECK, I WOULD NEED TO DO IT HERE.
        # # THE EASIEST WAY WOULD BE TO USE A DIFFERENT RETURN VALUE SO THAT I KNOW I NEED TO ADD CODE.
        # # I COULD ALSO PASS IN INITIAL NODE AND THE ONLY CHANGE I WOULD MAKE IS ADDING CODE TO THE NODE.

        #         # if there was an invocation, add the node to your current node
        #         if temp[1] == 1:
        #             # print("ENTERED ARG INVOCATION BLOCK")
        #             newNode = temp[0]
        #             # print("found a new invocation: " + str(newNode))

        #             # make sure you find the end of currNode before continuing
        #             while currNode.nextBlocks != []:
        #                 currNode = currNode.nextBlocks[0]
                    
        #             # now patch in the new invocation node
        #             currNode.nextBlocks.append(newNode)
        #             # make the current node the new one
        #             currNode = newNode


        #     currNode.nextBlocks.append(newFunctionNode.firstNode)
        #     currNode = newFunctionNode.firstNode
        #     # print("GOT THRU THAT SHIT")
        #     return (initial, 4)

        case m_assignment():
            # print("ASSIGNMENT CASE")
            # add the assignment code to the node
            currNode.code.append(expression)

            # # add the assignments nested code to the node
            # currNode.code.append(expression.source_expression) # REMOVED THIS
        
            # check for invocation inside the sub expression
            newTuple = checkForInvocation(expression.source_expression, currNode)
            currNode = newTuple[2]
            # print("currnode code: " + str(currNode.code))

        # SIMILAR ISSUE SHOWS UP HERE, NOT ADDING NESTED CODE TO THE NODE

            # if(newTuple[1] == 1):  
            #     tempNode = newTuple[0]
            #     currNode.nextBlocks.append(tempNode)
            #     newNode = CFG_Node(-1, [],[],[],blockId)
            #     blockId += 1
            
            #     # attach newNode to the end of the current link
            #     newTemp = tempNode
            #     while newTemp.nextBlocks != []:
            #         newTemp = newTemp.nextBlocks[0]
            #     newTemp.nextBlocks.append(newNode)

            # print("currNode code: " + str(currNode.code))
            # print("EXITING ASSIGNMENT CASE")
            return (currNode, 0)

        # case m_binop():
        #
        #     # # my thought is that if I reach a unary or binop inside of a guard, I will want to store the whole thing. MAYBE I JUST STORE THE WHOLE GUARD EXP
        #     # if ...:
        #     #     ...
        #
        #     # create a node for the left_expression and right_expression
        #     currNode = generate_CFG_Function_Handler([expression.left_expression, expression.right_expression], 1)
        #     # print("binop node code: " + str(currNode.code))
        #     return (currNode, 0)
        #
        # case m_unary():
        #     # print("ENTERED UNARY in generate_CFG_Node")
        #     # currNode.code.append(expression)
        #
        #     # # my thought is that if I reach a unary or binop inside of a guard, I will want to store the whole thing. MAYBE I JUST STORE THE WHOLE GUARD EXP
        #     # if ...:
        #     #     ...
        #
        #     # create a node for the operand_expression
        #     currNode = generate_CFG_Function_Handler([expression.operand_expression], 1)
        #     # print("unary node code: " + str(currNode.code))
        #     # currNode.code.append(expression)
        #     return (currNode, 0)

        # there shouldnt be anymore special case structs 
        case _:
            # print("other expression: " + str(expression))
            # add the code to the current list, continue to the next bit
            # USING THIS TO CATCH ANY CODE IN THE GUARD STATEMENT OF AN IF OR WHILE LOOP
            if(ifOrWhileFlag == 1):
                currNode.code.append(expression)
            return (currNode, 0)

# THIS IS WHERE YOU MADE THE CHANGE


# this function is used to check if an expression is an invocation and create a node for it. Also recursively travels the branches of the expression
def checkForInvocation(expression, currNode):
    # print("entered invocation check")
    global blockId
    match expression:
    #     case m_binop():
    #         # initially both left and right nodes are initially not invocation nodes
    #         leftFlag = 0
    #         rightFlag = 0
    #
    # # HERE IS WHERE I WOULD ADD CODE TO THE CURRENT NODE
    #         # currNode.code.append(expression.left_expression) # REMOVED THIS
    #         # currNode.code.append(expression.right_expression) # REMOVED THIS
    #
    #         # search the left expression for invocation
    #         temp = checkForInvocation(expression.left_expression, currNode)
    #         currNode = temp[2]
    #
    #
    #         # if you found invocation ...
    #         if temp[1] == 1:
    #             leftFlag = 1
    #             # create a leftNode
    #             leftNode = CFG_Node(-1, [], [], [], blockId)
    #             blockId += 1
    #
    #         # search the right expression for invocation
    #         temp = checkForInvocation(expression.right_expression, currNode)
    #         currNode = temp[2]
    #
    #
    #         # if you found invocation ...
    #         if temp[1] == 1:
    #             rightFlag = 1
    #             # create a rightNode
    #             rightNode = CFG_Node(-1, [], [], [], blockId)
    #             blockId += 1
    #
    #         # if you had an invocation in the left node
    #         if leftFlag == 1:
    #             # if you had an invocation in both nodes
    #             if rightFlag == 1:
    #                 # both sides had an invocation, merge them and return the merged node (left -> right)
    #                 leftNode.nextBlocks.append(rightNode)
    #                 return (leftNode, 1, currNode)
    #             # only the left one had an invocation, return the leftNode
    #             return (leftNode, 1, currNode)
    #
    #         # if you had an invocation in the right node
    #         elif rightFlag == 1:
    #             # only the right one had an invocation, return the rightNode
    #             return (rightNode, 1, currNode)
    #         # neither side had an invocation, return (None, 0)
    #         return (None, 0, currNode)
    #
    #
    #     case m_unary():
    #         # print("ENTERED UNARY in checkForInvocation")
    #         # search the op expression for invocation
    #
    #
    # # HERE IS WHERE I WOULD ADD CODE TO THE CURRENT NODE
    #         # currNode.code.append(expression.operand_expression) # REMOVED THIS
    #
    #         temp = checkForInvocation(expression.operand_expression)
    #         currNode = temp[2]
    #
    #
    #         # if you find invocation ...
    #         if temp[1] == 1:
    #             # create a unaryNode
    #             unaryNode = CFG_Node(-1, [], [], [], blockId)
    #             blockId += 1
    #             # return the unaryNode
    #             return (unaryNode, 1, currNode)
    #         return (None, 0, currNode)


        case m_invocation():
            currNode.code.append(expression)
            # get the node from the dict, change Id
    #         invocationNode = functionBlocks[expression.id.identifier].firstNode
    #         invocationNode.Id = blockId
    #         blockId += 1
            
    #         tempNode = invocationNode
            for exp in expression.args_expressions:
    #             # print("DID IN FACT ENTER THE LOOP")
    #             # print(str(exp))


    # # HERE IS WHERE I WOULD ADD CODE TO THE CURRENT NODE
    #             # currNode.code.append(exp) # REMOVED THIS
    #             currNode.code.append(expression)

                currTuple = checkForInvocation(exp, currNode)
                currNode = currTuple[2]

                
    #             if currTuple[1] == 1:
    #                 # print("ENTERED THE INNER IF: " + str(currTuple[0].code))
    #                 newTemp = currTuple[0]
    #                 newTemp.nextBlocks.append(tempNode)
    #                 tempNode = newTemp

            return (None, 1, currNode)

        case m_num() | m_new_struct() | m_null() | m_dot() | m_id():
        # case m_num() | m_bool() | m_new_struct() | m_null() | m_dot() | m_id() :
        #     currNode.code.append(expression)
            return (None, 0, currNode)

        # this case is used for catching stuff that might be in the guard statement and appending the code
        case m_bool() | m_binop() | m_unary():
            if ifOrWhileFlag == 1:
                currNode.code.append(expression)
            return (None, 0, currNode)

        # in case I missed any cases
        case _:
            # currNode.code.append(expression)
            # print("WHY DID YOU GET HERE? Expression: " + str(expression))
            return (None, 0, currNode)

