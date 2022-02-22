import unittest
from ast_class_definitions import *
# from cfg_generator import *
import test_ast_trees


# GLOBAL FUNCTION BLOCK ENVIRONMENT
functionBlocks = {} 
blockId = 0


# REMOVE returnType FROM THE CFG_Node AND ADD IT TO FUNCTION NODES???????

class CFG_Node:
    def __init__(self, previousBlocks:list, nextBlocks:list, code:list, id:int, returnType = None): 
        self.previousBlocks = previousBlocks # can be multiple
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

        # need to update next value of the previous node(s)
        if updateFlag == 1:
            # step through the tempPrevNodes and update next
            for node in tempPrevNodes:
                node.nextBlocks.append(currNode)
                print("REACHED")
            
            # reset updateFlag
            updateFlag = 0

            # empty tempPrevNodes
            tempPrevNodes = []




        # might be a weird edge case on the last statement
        # check if we need a new node (if or while)
        if(currTuple[1] > 1):
            
            tempPrevNodes = []

            # if you currently have a node that is not empty ...
            if currNodeCount > 0:  
                # add the tempNode to the linked list before you get rid of it for good
                tempNode.nextBlocks.append(currNode)
                currNode.previousBlocks.append(tempNode)

                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = tempNode
                
                
            
            currNodeCount = 0

            newNode = CFG_Node([], [], [], blockId)
            blockId += 1
            
            # while statement, connect the returned guard node to the new node
            if(currTuple[1] == 2):
                
                tempNode.nextBlocks.append(currNode)

#                 # simply put the newNode as a nextBlock from currNode and ...
#                 currNode.nextBlocks.append(newNode) # WHAT IF THE NEW NODE IS NEVER FILLED IN????
# # FIX THIS ABOVE LINE


                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode

                # put the currNode as a previous block from the newNode
                newNode.previousBlocks.append(currNode)

                # update currNode to be newNode
                currNode = newNode


                # set the current final block to the guard statement
                currFinalBlocks = [currNode] # THIS MAY NOT BE THE CORRECT INTERPRETATION

                # we will later need to refer to this node
                tempPrevNodes.append(currNode)
                updateFlag = 1

            # if else statement, connect each existing next from the guard block to the new node
            else:


                # tempNode.nextBlocks.append(currNode)


                
                # if this is our first node, set it to initial node
                if initialFlag == 0:
                    initialFlag = 1
                    initialNode = currNode


                # get the if node and also the else node if it exists
                ifNode = currNode.nextBlocks[0]



#                 # simply put the newNode as a nextBlock from both the if and else Nodes and ...
#                 ifNode.nextBlocks.append(newNode)
# # FIX THIS ABOVE LINE



                # put the if node and else nodes as previous blocks from the newNode
                newNode.previousBlocks.append(ifNode)

                # set the current final block to the if statement
                currFinalBlocks = [ifNode] 

                # do all the same for the else node if it exists
                if len(currNode.nextBlocks) > 1:
                    elseNode = currNode.nextBlocks[1]


                    # elseNode.nextBlocks.append(newNode)
# FIX THIS ABOVE LINE


                    newNode.previousBlocks.append(elseNode)

                    # add the else block to current final blocks
                    currFinalBlocks.append(elseNode)

                # update currNode to be newNode
                currNode = newNode

                # we will later need to refer to this node
                tempPrevNodes.append(ifNode)
                tempPrevNodes.append(elseNode)
                updateFlag = 1


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

            ifNode.previousBlocks.append(guardNode)
            

            print("\n\n\n\n" + str(expression.else_statements) + "\n\n\n\n")
            # check if there is an else
            if expression.else_statements != [None]:
                print("\n\n\n\nTESTING\n\n\n\n")

                # call generate_CFG_Nodes on this new branch with its statements and also set this to next from the guard node
                elseNode = generate_CFG_Function_Handler(expression.else_statements, 1)
                if(elseNode == None):
                    return None
                guardNode.nextBlocks.append(elseNode)
                elseNode.previousBlocks.append(guardNode)
                
                # add the else statements
                # elseNode.code.append(expression.else_statements) # This should actually already be done


            currNode.nextBlocks.append(guardNode)
            guardNode.previousBlocks.append(currNode)


            # somehow we need to set the next of both if and else to the next statement
                # shouldnt this be done in the upper level function?


            # what should we return?

            return (guardNode, 3) # make sure this is actually what you want


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
            whileNode.nextBlocks.append(guardNode)

            # return the guard node
            return (guardNode, 2)


        # ret → return {expression}opt;
        case m_ret():
            print("return case")
            # set the return type of the current node
            # STILL NEED TO DO THIS ???? 
            currNode.returnType = ... # MIGHT NEED SOME SORT OF FUNCTION TO GET THE TYPE FROM me_ret.expression

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
                newNode.previousBlocks.append(currFinalNode)


            # I DONT THINK I NEED TO DO ANYTHING SPECIAL AFTER RETURN 
            # my thought here is that since we dont need to make a new node in the above level function, we can just return the newNode
            return (newNode, 0) # WAS 2 HERE NOW IS 0


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






