import unittest
from ast_class_definitions import *
# from cfg_generator import *
import test_ast_trees


# GLOBAL FUNCTION BLOCK ENVIRONMENT
functionBlocks = {} 
blockId = 0


# REMOVE returnType FROM THE CFG_Node AND ADD IT TO FUNCTION NODES???????

class CFG_Node:
    # def __init__(self, nextBlocks:list, code:list, id:int, returnType = None): 
    def __init__(self, previousBlocks:list, nextBlocks:list, code:list, id:int, returnType = None): 
        # self.previousBlocks = previousBlocks # can be multiple
        self.nextBlocks = nextBlocks # could be multiple
        self.code = code
        self.id = id
        self.returnType = returnType # default is currently None, might wanna do m_type("void") instead, also should probably add a type


# DO YOU NEED RETURN TYPE????
class Function_Nodes:
    def __init__(self, firstNode:CFG_Node, lastNodes:list[CFG_Node], returnType = None): 
        self.firstNode = firstNode
        self.lastNodes = lastNodes
        self.returnType = returnType


def generate_CFG_Prog_Handler(program:m_prog):
    global blockId
    print("entered Prog_Handler")
    # look through the functions and make them into blocks (in order)
    for fun in program.functions:
        # if you get to main, break, this is a special case (??)
        if(fun.id.identifier) == "main":
            # print("\n\ncheck main")
            print("function name: " + fun.id.identifier)
            mainFun = fun
            break
        print("function name: " + fun.id.identifier)
        # create block for each function
        newNode = generate_CFG_Function_Handler(fun.statements, 0)

        # add the new block to the environment
        functionBlocks[fun.id.identifier] = newNode


    # once we get to main we will continue making blocks but also piecing together the other functions
    # WHAT DO WE DO WITH MAIN HERE

    # print("LOOK HERE: " + str(mainFun.statements))

    mainNode = generate_CFG_Function_Handler(mainFun.statements, 0)

    # print(str(functionBlocks))

# DONT NEED MAIN SPECIAL CASE


    print("\n\nENTERING NODE REMOVAL\n\n")

    queue = []
    nodeReferences = {}
    # enqueue the node at the front
    queue.append( mainNode.firstNode )
    updatePrevFlag = 1

    # prevNode = None # this would cause errors

    # step through the nodes and delete the empty nodes by patching the others together
    # j = 0
    firstFlag = 1
    while queue != []:
        # j += 1
        currNode = queue.pop(0)

        # if currNode.id == 2:
        #     print(str(currNode.nextBlocks))
        print("currID: " + str(currNode.id) )
        # print("currID: " + str(currNode.id) +  " Queue Size: " + str(len(queue)) + " Queue: " + str(queue))


        # if j == 15:
        #     quit()

        # if current node is none, we assume we are at the first node, and continue
        if currNode.code == [] and firstFlag == 1:
            firstFlag = 0
            print("1 removing node number: " + str(currNode.id))

            # the weird empty node branches into 2+
            if len(currNode.nextBlocks) > 1:
                print("\n\n\n\nNO IDEA WHAT I SHOULD DO IN THIS CASE \n\n\n\n")
                return None

            # the empty node has no next blocks, I guess just return it
            if len(currNode.nextBlocks) == 0:
                print("\n\n\n\nNO IDEA WHAT I SHOULD DO IN THIS CASE \n\n\n\n")
                return mainNode

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
            if currNode.nextBlocks[i].code == []:
                print("2 removing node number: " + str(currNode.nextBlocks[i].id))
                print("removed node nextBlocks: " + str(currNode.nextBlocks[i].nextBlocks))
                
                # add the nextBlocks of that node to the current one
                for node in currNode.nextBlocks[i].nextBlocks:
                    print("Here")
                    currNode.nextBlocks.append(node)

                # remove the node
                currNode.nextBlocks.pop(i)
                # continue, dont increment i as it is now removed
                firstFlag = 0
                continue 

            i += 1



                            # # if str(currNode.code) not in nodeReferences:
                            # if str(currNode.id) not in nodeReferences:
                            #     # print("check1")
                            #     # nodeReferences[str(currNode.code)] = 1
                            #     nodeReferences[str(currNode.id)] = (1, currNode)

        firstFlag = 0

        # add all the next nodes to the queue
        for node in currNode.nextBlocks:
            queue.append(node)


        # else:
        #     # print("check2\n")
        #     # nodeReferences[str(currNode.code)] = nodeReferences[str(currNode.code)] + 1
        #     nodeReferences[str(currNode.id)] = (nodeReferences[str(currNode.id)][0] + 1, currNode)  # DOUBLE CHECK

        # print(currNode.code)

        # for node in currNode.nextBlocks:
        #     print("nextNode id: " + str(node.id))

        # for node in currNode.previousBlocks:
        #     print("prevNode id: " + str(node.id))

        # # there is no code, this block is worthless, patch the previous and next nodes together
        # if node.code == []:
            
#             # check if there is a previous node
#             if node.previousBlocks != []:
#                 # remove the current node from the previous block next values
#                 for prevNode in node.previousBlocks:
#                     print("\n\n" + str(prevNode.id))
#                     print(str(nodeReferences) + "\n")
#                     tempPrevNode = nodeReferences[str(prevNode.id)][1]

# # DEBUG THIS, YOU STOPPED HERE
#                     tempPrevNode.nextBlocks.remove(node.id)

#                     # update the previous block next values to include the current block next values
#                     for newID in node.nextBlocks:
#                         tempPrevNode.nextBlocks.append(newID)




#             # check if there is a next node
#             if node.nextBlocks != []:
#                 # remove the current block from the previous list of each next node
#                 for ID in node.nextBlocks:
# # ID IS CURRENTLY ACTUALLY A NODE ????

#                     tempNextNode = nodeReferences[str(ID)][1]
#                     # tempNextNode.previousBlocks.remove(node.id) # WAS IN

#                     # WAS IN
#                     # # update the previous list of each next node to be the previous blocks of the current node 
#                     # for newID in node.previousBlocks:
#                     #     tempNextNode.previousBlocks.append(newID)






        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.id)]) + "\nblock Id: " + str(currNode.id) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.code)]) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) +       "\n\n\n")# + "\nnumReferences: " + str(nodeReferences[nodeNum]) + "\n\n\n")

        # # update the previoud node
        # if updatePrevFlag == 1:
        #     prevNode = currNode

        # # previous node was garbage, dont change it
        # else:
        #     updatePrevFlag = 1



    print("\n\nEXITING NODE REMOVAL\n\n")





    return mainNode
    # return newNode

    



# the function flag tells us if we should create a function node or just a node (0 means function, 1 means not function)
# handle each function uniquely, step through statements and create/connect nodes as needed
def generate_CFG_Function_Handler(currStatements:list, functionFlag:int): # WAS def generate_CFG_Function_Handler(currFunction:m_function):
    global blockId
    print("entered Function_Handler with flag " + str(functionFlag))
    # create a node
    currNode = CFG_Node([], [], [], blockId)
    blockId += 1

    currFinalBlocks = []

    initialNode = currNode # need to update this
    initialFlag = 0

    if functionFlag == 0:
        functionNode = Function_Nodes(None, [], None) # return type probably wrong here
    
    # currNode = None
    currNodeCount = 0
    updateFlag = 0
    # run this node through the statements until we need a new one
    for statement in currStatements:


        # CONSIDER JUST PUTTING THE generate_CFG_Nodes() FUNCTION CODE HERE INSTEAD OF CALLING IT
            # THIS WOULD FIX THE ISSUE WHERE WE CANT PASS BY ADDRESS, ONLY REFERENCE
            # I may not need to do this but I am unsure at the moment

        
        # add to curr node based on current statement
        # NOTE: if we look at an if else/while statement, we return the guard node so that we can connect the nodes
        currTuple = generate_CFG_Nodes(statement, currNode)

        # save the previous node in case its been replaced
        tempNode = currNode

        # i need to do this since python doesnt pass by reference
        currNode = currTuple[0]
        # print("\ncurr Node: " + str(currNode.code))

        # # need to update next value of the previous node(s)
        # if updateFlag == 0:
        #     # step through the tempPrevNodes and update next

        # might be a weird edge case on the last statement
        # check if we need a new node (if or while)
        if(currTuple[1] > 1):
            
            # if you currently have a node that is not empty ...
            if currNodeCount > 0:  
                # add the tempNode to the linked list before you get rid of it for good
                # tempNode.nextBlocks.append(currNode) # WAS IN
                # currNode.previousBlocks.append(tempNode) # WAS IN

                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = tempNode
                
                
            
            currNodeCount = 0

            newNode = CFG_Node([], [], [], blockId)
            blockId += 1
            
            # while statement, connect the returned guard node to the new node
            if(currTuple[1] == 2):
                
                # tempNode.nextBlocks[0].nextBlocks.append(currNode)
                tempNode.nextBlocks.append(currNode)
                
                currNode.nextBlocks[0].nextBlocks.append(newNode)

                # simply put the newNode as a nextBlock from currNode and ...
                currNode.nextBlocks.append(newNode) # WHAT IF THE NEW NODE IS NEVER FILLED IN????
# FIX THIS ABOVE LINE


                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # WAS IN
                # # put the currNode as a previous block from the newNode
                # newNode.previousBlocks.append(currNode)

                # update currNode to be newNode
                currNode = newNode


                # set the current final block to the guard statement
                currFinalBlocks = [currNode] # THIS MAY NOT BE THE CORRECT INTERPRETATION



            # if else statement, connect each existing next from the guard block to the new node
            else:


                # tempNode.nextBlocks.append(currNode)


                
                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode


                # get the if node and also the else node if it exists
                ifNode = currNode.nextBlocks[0]



                # simply put the newNode as a nextBlock from both the if and else Nodes and ...
                ifNode.nextBlocks.append(newNode)
# FIX THIS ABOVE LINE


                # WAS IN
                # # put the if node and else nodes as previous blocks from the newNode
                # newNode.previousBlocks.append(ifNode)

                # set the current final block to the if statement
                currFinalBlocks = [ifNode] 

                # do all the same for the else node if it exists
                if len(currNode.nextBlocks) > 1:
                    elseNode = currNode.nextBlocks[1]


                    elseNode.nextBlocks.append(newNode)
# FIX THIS ABOVE LINE

                    # WAS IN
                    # newNode.previousBlocks.append(elseNode)

                    # add the else block to current final blocks
                    currFinalBlocks.append(elseNode)

                # update currNode to be newNode
                currNode = newNode


# SHOULD BE CAUGHT IN TYPE CHECKER
        # reached function invocation error in block
        elif(currTuple[1] == -1):
            # there are no valid nodes to return (make sure this is what you want)
            return None
            

        # reached return in main block
        elif(currTuple[1] == 1):

            if initialFlag == 0:
                initialFlag = 1
                initialNode = currTuple[0]

            # the current final block is currTuple[0]
            currFinalBlocks = [currTuple[0]]

            # break from the function, no need to go further (shouldnt really be any more in reality)
            break

        else:
            currNodeCount += 1
    

    # if this is our first node, set it to initial node
    if initialFlag == 0:
        initialNode = currNode


    # here we return the function node
    if functionFlag == 0:
        functionNode.firstNode = initialNode
        functionNode.lastNodes = currFinalBlocks
        return functionNode 

    # youve reached the end of the function, return the intial node
    return initialNode

        






# add the code to the current node, if and while will do weird things
# DO I WANT TO CALL THIS WITH MULTIPLE EXPRESSIONS???? OR JUST 1 AT A TIME??

# returns a tuple that is (node, int) - 
    # return 0 if you can just continue
    # 1 if it is a return statement
    # 2 if it is an invocation
    # 3 if it is a while statement 
    # 4 if it is an if/if else statement
# add to the current node, when you get 
def generate_CFG_Nodes(expression, currNode):
    global blockId
    print("entered low level CFG function")
    match expression:

        # conditional → if ( expression ) block {else block}opt
        # GUARD statement IS ITS OWN BLOCK
        case m_conditional():
            print("conditional case")
            # call generete_CFG_Nodes on the guard statement, set this to next from the current node

            # currTuple = generate_CFG_Function_Handler([expression.guard_expression], 1) # DOUBLE CHECK SYNTAX
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1) # DOUBLE CHECK SYNTAX

            # if you got a function environment error
            if(guardNode == None):
                # make sure this is what you want
                return None

            # guardNode = currTuple[0]

            # add the guard statement
            # guardNode.code.append(expression.guard_expression) # This should actually already be done


            # call generete_CFG_Nodes on the new branch, set this to next from the guard node
            ifNode = generate_CFG_Function_Handler(expression.if_statements, 1)
            if(ifNode == None):
                return None

            # add the if statements
            # ifNode.code.append(expression.if_statements) # This should actually already be done

            guardNode.nextBlocks.append(ifNode)

            # WAS IN
            # ifNode.previousBlocks.append(guardNode)
            

            print("\n\n\n\n" + str(expression.else_statements) + "\n\n\n\n")
            # check if there is an else
            if expression.else_statements != [None]:
                print("\n\n\n\nTESTING\n\n\n\n")

                # call generate_CFG_Nodes on this new branch with its statements and also set this to next from the guard node
                elseNode = generate_CFG_Function_Handler(expression.else_statements, 1)
                if(elseNode == None):
                    return None
                guardNode.nextBlocks.append(elseNode)
                # WAS IN
                # elseNode.previousBlocks.append(guardNode)
                
                # add the else statements
                # elseNode.code.append(expression.else_statements) # This should actually already be done


            currNode.nextBlocks.append(guardNode)
            # WAS IN 
            # guardNode.previousBlocks.append(currNode) 


            # somehow we need to set the next of both if and else to the next statement
                # shouldnt this be done in the upper level function?


            # what should we return?

            return (guardNode, 3) # make sure this is actually what you want


# FIX THIS ISSUE
# NOTE: YOU DO NOT WANT TO PUT THE NEXT BLOCK OF THE WHILE BODY TO THE GUARD STATEMENT

        # loop → while ( expression ) block
        # GUARD statement IS ITS OWN BLOCK
        case m_loop():
            print("loop case")
            # call generete_CFG_Nodes on the guard statement, set this to next from the current node
            # currTuple = generate_CFG_Function_Handler([expression.guard_expression], 1)
            guardNode = generate_CFG_Function_Handler([expression.guard_expression], 1)
            # guardNode = currTuple[0]
            if guardNode == None:
                return None

            # add the guard code
            # guardNode.code.append(expression.guard_expression) # This should already be done

            # call generete_CFG_Nodes on the statement in the while
            whileNode = generate_CFG_Function_Handler(expression.body_statements, 1)
            # whileNode = currTuple[0]
            if whileNode == None:
                return None
            
            # add the while statements
            # whileNode.code.append(expression.body_statements) # This should already be done

            # its next should be the while statements and also the code after it
            # set this to next from the guard node, next from this should also be the guard node
            guardNode.nextBlocks.append(whileNode)
            # whileNode.nextBlocks.append(guardNode)

            # return the guard node
            return (guardNode, 2)


        # ret → return {expression}opt;
        case m_ret():
            print("return case")
            # set the return type of the current node
            # STILL NEED TO DO THIS ???? 
            # currNode.returnType =  ... # MIGHT NEED SOME SORT OF FUNCTION TO GET THE TYPE FROM me_ret.expression



# DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE EXPRESSION?????



            # THIS MAY BE A SECOND TIME OF ADDING THIS CODE TO THE BLOCK
            currNode.code.append(expression)



            return (currNode, 1)



# THIS FUNCTION ISNT DONE YET
        # THINK MORE ABOUT HOW YOU WILL RETURN FROM THIS CASE
        # invocation → id arguments ;
        case m_invocation():
            print("invocation case")
            # function not in environment case
            if(expression.id.identifier not in functionBlocks):
                return (currNode, -1)

            # add the invocation code
            currNode.code.append(expression)
            
            # DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE ARGUMENT EXPRESSIONS????
            for exp in expression.args_expressions:
                currTuple = generate_CFG_Nodes(exp, currNode)
                currNode = currTuple[0]

            # patch the node from the dictionary on the current head


            # get a copy of the node that is in the function block dictionary
            newFunctionNode = functionBlocks[expression.id.identifier]
            

            # patch in the next nodes to the current block (first in the function node)
            currNode.nextBlocks = [newFunctionNode.firstNode]


            # have to create a newNode so that I can set the nextNode of all of the final nodes in the functionNode
            # NOTE: We dont have to create a new node in the upper level function because we do it here
            newNode = CFG_Node([], [], [], blockId)
            blockId += 1


            # step through each last node in the function and set the next nodes for each to the new node
            for currFinalNode in newFunctionNode.lastNodes:
                currFinalNode.nextBlocks = [newNode]
                # WAS IN
                # newNode.previousBlocks.append(currFinalNode)



# # DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE ARGUMENT EXPRESSIONS????
#             for exp in expression.args.expressions:
#                 currNode = generate_CFG_Nodes(exp, currNode)


            # I DONT THINK I NEED TO DO ANYTHING SPECIAL AFTER RETURN 
            # my thought here is that since we dont need to make a new node in the above level function, we can just return the newNode
            return (newNode, 0) # WAS 2 HERE NOW IS 0


        # which other things potentially have expressions hidden in them?
        # assignment
        # binop
        # unary


        case m_assignment():
# DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE EXPRESSION
            
            currTuple = generate_CFG_Nodes(expression.source_expression, currNode) 
            currNode = currTuple[0]

            
            return (currNode, 0)


        case m_binop():
# DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE LEFT AND RIGHT EXPRESSION

            currTuple = generate_CFG_Nodes(expression.left_expression, currNode)
            currNode = currTuple[0]
            currTuple = generate_CFG_Nodes(expression.right_expression, currNode)
            currNode = currTuple[0]

            return (currNode, 0)


        case m_unary():
# DO I NEED TO RECURSIVELY CALL THIS FUNCTION ON THE EXPRESSION

            currTuple = generate_CFG_Nodes(expression.operand_expression, currNode)
            currNode = currTuple[0]


            return (currNode, 0)



        # there shouldnt be anymore special case structs 
        case _:
            print("other expression: " + str(expression))
            # add the code to the current list, continue to the next bit
            currNode.code.append(expression)
            return (currNode, 0)




# # step through each node and print the head
# def printCFG(head):
#     print("-----------------------------------\nEntered Print Function\n-----------------------------------\n")
#     # probably breadth first search (queue) instead of depth (stack)
#     nodeNum = 0
#     nodeLevel = 0

#     # print(head.code)

#     queue = []

#     nodeReferences = {}

#     queue.append( (head, nodeLevel) )

#     while queue != []:
#         currTuple = queue.pop()
#         currNode = currTuple[0]

#         if nodeLevel <= currTuple[1]:
#             print("check0\n")
#             nodeLevel += 1


#         if str(currNode.code) not in nodeReferences:
#             print("check1\n")
#             nodeReferences[str(currNode.code)] = 1

#             for node in currNode.nextBlocks:
#                 print("check3")
#                 queue.append( (node, nodeLevel + 1) )


#         else:
#             print("check2\n")
#             nodeReferences[str(currNode.code)] = nodeReferences[str(currNode.code)] + 1


#         print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.code)]) + "\n\n\n")
#         # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) +       "\n\n\n")# + "\nnumReferences: " + str(nodeReferences[nodeNum]) + "\n\n\n")
#         nodeNum += 1


# def main():
#     # # simple case
#     # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected3)
#     # printCFG(testCFG.firstNode)

#     # # invocation case
#     # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected7)
#     # printCFG(testCFG.firstNode)

#     # # if case
#     # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected5)
#     # printCFG(testCFG.firstNode)
    
#     # while case 
#     testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected4)
#     printCFG(testCFG.firstNode)


# if __name__ == "__main__":
#     main()






