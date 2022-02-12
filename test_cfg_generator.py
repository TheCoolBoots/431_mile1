import unittest
from ast_class_definitions import *
from cfg_generator import *
from json_parser import *
from generateLLVM import *
import test_ast_trees
import json
import os
from ssaGenerator import *

# NOTE: YOU WILL WANT TO HAVE A NODE AT THE START OF THE CFG FOR INITIALIZATION PURPOSES LATER

# YOU WILL NEED  A WAY TO PASS ALONG ALL OF THE FUNCTIONS HEAD NODES IN A LIST SO THAT THEY ARE EASY TO GRAB

# FOR EACH ONE YOU WILL NEED TO CREATE A MAPPING FOR EACH PARAMETER OF THE FUNCTION



# step through the node tree and print a formatted dot file
def dotToCFG(head, name):
    # nodeId = 0 # consider implementing this, the issue came when trying to check the id of the next node
    # a potential solution is to walk thru the nodes and update the id number of each and then run thru again
    # and print out all of the connections.


    # # initialize dict for nodes
    # nodeReferences = {}

    # # initialize queue with head node
    # queue = []
    # queue.append(head)





# # SOMEWHERE I NEED TO GET THE ENVIRONMENTS SO THAT I CAN USE statementToLLVM()
# # LOOK AT WHAT toLLVM does with environments, and consider doing that same thing

    # while queue != []:
    #     currNode = queue.pop(0)

    #     currRegister = 0
    #     currLLVM = str(currNode.id) + " note(label = "
    #     for statement in currNode.code:
    #         match expression:
    #             case m_invocation:
    #                 # update the llvm string with current code and then add a new line
    #                 currLLVM = currLLVM + CURRENTCODE + "\l"
    #             case _:
                    
    #         # currTuple = statementToLLVM(currRegister, ___, ___, ___, ___)
    #         # currRegister = currTuple[0]

    #         # # print the LLVM code for each node
    #         # # a note(label = ___ ___ ___) # HOW SHOULD THIS LABELS BE SEPERATED??? COMMAS???? 
    #         # for item in currTuple[2]:
    #         #     currLLVM = currLLVM + item + " "
             

    #     # expression always returns a value
    #     # statement is anything that must run
    #         # statement recursively calls expressionToLLVM, so I dont need to add unary, binop, num, bool, ...

        





    # print out the header of the file
    print("digraph \"" + name + "\" {" )

    # initialize dict for nodes
    nodeReferences = {}

    # initialize queue with head node
    queue = []
    queue.append(head)

    # loop through the nodes and print a line for each connection
    while queue != []:
        currNode = queue.pop(0)

        # only print and add the new nodes to the queue if the node hasnt been traversed
        if currNode in nodeReferences:
            continue
        # log each node/connection so that you dont traverse twice
        else:
            nodeReferences[currNode] = True

        # print each path from the current node
        for node in currNode.nextBlocks:
            print("  " + str(currNode.id) + " -> " + str(node.id) + ";") # DOUBLE CHECK
            # print("  " + str(nodeId) + " -> " + str(node.id) + ";") # DOUBLE CHECK
            queue.append(node)
            # nodeId += 1
    
    # print out the footer of the file
    print("}")

    # return empty
    return



# given the head block of a function, step through and add previous blocks for each node
def addPreviousBlocks(head):
    # make a queue of nodes to visit - start at the head
    queue = [head]

    # keep track of visited nodes (dict)
    visitedDict = {}

    # search the queue while it isnt empty
    while(queue != []):
        # pop the front
        curr = queue.pop(0)

        if curr in visitedDict:
            continue
        else:
            visitedDict[curr] = True

        # add curr as a previous block
        for node in curr.nextBlocks:
            # THESE TWO SOLUTIONS SHOULD BE EQUIVALENT, IM JUST NOT 100% CONFIDENT IN "not in"

            # add the current node to the previousBlocks list
            if(curr not in node.previousBlocks):
                node.previousBlocks.append(curr)

            # if (curr in node.previousBlocks):
            #     pass
            # else:
            #     node.previousBlocks.append(curr)

            if node not in visitedDict:
                queue.append(node)


    return head




# add an empty block at the start and end of each while as well as the start and end of each if/else
# also add a return block for stack cleanup
# dont worry about just if ??
def addEmptyBlocks(head):


    queue = [head]
    nodeDict = {}


#NOTE: there is a weird case where an if-else leads into a while guard. This while guard node would have 3
# previous blocks. However, while walking through the tree, you should reach the if else convergence point before
# you reach the while node.
    # step through every node in the tree
    while queue != []:
        currNode = queue.pop(0)

        if currNode in nodeDict:
            continue

        falseCount = 0
        prevBlocks = len(currNode.previousBlocks)
        nextBlocks = len(currNode.nextBlocks)

        # use this dict to find which node is the body for the guard
        currNodeDict = {}
        for tempNode in currNode.previousBlocks:
            currNodeDict[tempNode] = True

        for tempNode in currNode.nextBlocks:
            # if it is the body, make the value False
            if tempNode in currNodeDict:
                falseCount += 1
                currNodeDict[tempNode] = False

            # if it is the true next node, make the value True
            else:
                currNodeDict[tempNode] = True

        # KEEP IN MIND, THIS MIGHT BE A SPECIAL CASE SO WE MUST TREAT IT AS SUCH.
        # ADD THE NEW NODE BEFORE THIS ONE AND THEN REQUEUE THE NODE.
        # THIS IS NECESSARY WHEN THE NODE IS BOTH AN IF CONVERGENCE AND WHILE GUARD.
        # it is an if block convergence point if it has two prev blocks (could it have more? is there anything I need to be careful about?)
        if (prevBlocks == 2 and falseCount == 0) or (prevBlocks == 3 and falseCount == 1)
            # add a node before the block since you want the if and else to converge on a single empty node

            # -2 will signify empty prev (for now)
            newPrevNode = CFG_Node([], [], [], -2)

            newPrevNode.nextBlocks = [currNode]

            for tempNode in currNode.previousBlocks:
                if currNodeDict[tempNode] == True:
                    newPrevNode.previousBlocks.append(tempNode)
                    tempNode.nextBlocks = [newPrevNode]

                else:
                    currNode.previousBlocks = [tempNode]

                currNode.previousBlocks.append(newPrevNode)

            queue.append(currNode)
            continue



        # it is a while block if it has a false count. This means that 1 of the prev and next blcoks are the same
        # it is a while block if it has 2 next blocks and 2 prev blocks (could even look at a prev block being the same as a next block)
        elif falseCount > 0:

            # -2 will signify empty prev (for now)
            newPrevNode = CFG_Node([], [], [], -2)
            # -1 will signify empty next (for now)
            newNextNode = CFG_Node([], [], [], -1)


            # fix up the previous and next block lists for both temp node and the new node
            for tempNode in currNode.previousBlocks:
                if currNodeDict[tempNode] == True:
                    newPrevNode.previousBlocks.append(tempNode)
                    tempNode.nextBlocks = [newPrevNode]

                else:
                    currNode.previousBlocks = [tempNode]

            currNode.previousBlocks.append(newPrevNode)

            for tempNode in currNode.nextBlocks:
                if currNodeDict[tempNode] == True:
                    newNextNode.nextBlocks.append(tempNode)
                    tempNode.previousBlocks = [newNextNode]

                else:
                    currNode.nextBlocks = [tempNode]

            currNode.previousBlocks.append(newNextNode)





        # it is an if block guard if it has 2 next blocks and none of the prev blocks are the same as the next blocks
        # this will catch both if-else and just plain if structures since both need to have two next blocks
        elif nextBlocks >= 2 and falseCount == 0:  # will it ever be greater than 2?? nah
            # add a node before the guard

            # -2 will signify empty prev (for now)
            newPrevNode = CFG_Node([], [], [], -2)


            newPrevNode.nextBlocks = [currNode]

            for tempNode in currNode.previousBlocks:
                # if currNodeDict[tempNode] == True:
                newPrevNode.previousBlocks.append(tempNode)
                tempNode.nextBlocks = [newPrevNode]

                # else:
                #     currNode.previousBlocks = [tempNode]

            currNode.previousBlocks.append(newPrevNode)




        # # just a regular block, no need to do anything special
        # else:
        #     # do anything????

        nodeDict[currNode] = True

        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)




    # walk back thru and for each return block add a next block that goes to the same place
        # for each node you will step through the lines of code

        # if a line of code is an m_ret, link the block to the only return block (instead of the other block??? or as well as??? I think instead.)






    # finally add an initial block at the start that is empty




    return head




# step through each node and print the head
def printCFG(head):
    print("-----------------------------------\nEntered Print Function\n-----------------------------------\n")
    # probably breadth first search (queue) instead of depth (stack)
    nodeNum = 0
    nodeLevel = 0

    # print(head.code)

    queue = []

    nodeReferences = {}

    queue.append( (head, nodeLevel) )

    while queue != []:
        currTuple = queue.pop(0)
        currNode = currTuple[0]

        if nodeLevel <= currTuple[1]:
            # print("check0")
            nodeLevel += 1


        # if str(currNode.code) not in nodeReferences:
        if str(currNode.id) not in nodeReferences:
            # print("check1")
            # nodeReferences[str(currNode.code)] = 1
            nodeReferences[str(currNode.id)] = 1

            for node in currNode.nextBlocks:
                # print("check3")
                queue.append( (node, nodeLevel + 1) )


        else:
            # print("check2\n")
            # nodeReferences[str(currNode.code)] = nodeReferences[str(currNode.code)] + 1
            nodeReferences[str(currNode.id)] = nodeReferences[str(currNode.id)] + 1

        print(currNode.code)

        for node in currNode.nextBlocks:
            print("nextNode id: " + str(node.id))

        for node in currNode.previousBlocks:
            print("prevNode id: " + str(node.id))

        # WAS IN
        # for node in currNode.previousBlocks:
        #     print("prevNode id: " + str(node.id))

        print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.id)]) + "\nblock Id: " + str(currNode.id) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.code)]) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) +       "\n\n\n")# + "\nnumReferences: " + str(nodeReferences[nodeNum]) + "\n\n\n")
        
        nodeNum += 1


def main():
    # # simple function case
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected3)
    # testCFGa = functionList[-1]
    # testCFGa.firstNode = addPreviousBlocks(testCFGa.firstNode)
    # # printCFG(testCFGa.firstNode)
    # dotToCFG(testCFGa.firstNode, "trivial case")


    # # invocation case
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected7)
    # testCFGb = functionList[-1]
    # testCFGb.firstNode = addPreviousBlocks(testCFGb.firstNode)
    # # printCFG(testCFGb.firstNode)
    # dotToCFG(testCFGb.firstNode, "simple invocation case")


    # # if case => if.mini
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected5)
    # length = len(functionList)
    # testCFGc = functionList[length-1]
    # testCFGc.firstNode = addPreviousBlocks(testCFGc.firstNode)
    # # printCFG(testCFGc.firstNode)
    # dotToCFG(testCFGc.firstNode, "simple if case")
    

    # # good for now, may think more about functions that have no return statement later on
    # # while case => loop.mini
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected4)
    # length = len(functionList)
    # testCFG0 = functionList[length-1]
    # testCFG0.firstNode = addPreviousBlocks(testCFG0.firstNode)
    # # printCFG(testCFG0.firstNode)
    # dotToCFG(testCFG0.firstNode, "simple while case")


    # # simplest case of if else, print statement in each
    # with open('json_parser_tests/ifelse.json') as file1:
    #     contents = json.load(file1)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG1 = functionList[length-1]
    # testCFG1.firstNode = addPreviousBlocks(testCFG1.firstNode)
    # # printCFG(testCFG1.firstNode)
    # dotToCFG(testCFG1.firstNode, "simple if else case")

    # # lgtm
    # # while and then if-else case
    # with open('json_parser_tests/loop_if.json') as file2:
    #     contents = json.load(file2)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG2 = functionList[length-1]
    # testCFG2.firstNode = addPreviousBlocks(testCFG2.firstNode)
    # # printCFG(testCFG2.firstNode)
    # dotToCFG(testCFG2.firstNode, "while and then if-else case")


    # # lgtm
    # # if and then while loop case
    # with open('json_parser_tests/if_loop.json') as file3:
    #     contents = json.load(file3)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG3 = functionList[length-1]
    # testCFG3.firstNode = addPreviousBlocks(testCFG3.firstNode)
    # printCFG(testCFG3.firstNode)
    # # dotToCFG(testCFG3.firstNode, "if and then while loop case")


    # # looks good
    # # invocation case 2
    # with open('json_parser_tests/myFunctionCall.json') as file4:
    #     contents = json.load(file4)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG4 = functionList[length-1]
    # testCFG4.firstNode = addPreviousBlocks(testCFG4.firstNode)
    # printCFG(testCFG4.firstNode)
    # # dotToCFG(testCFG4.firstNode, "simple invocation case")


    # # looks good
    # # invocation case 3
    # with open('json_parser_tests/harderFunctionCall.json') as file5:
    #     contents = json.load(file5)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG5 = functionList[length-1]
    # testCFG5.firstNode = addPreviousBlocks(testCFG5.firstNode)
    # printCFG(testCFG5.firstNode)
    # # dotToCFG(testCFG5.firstNode, "two invocation case")


    # # lgtm
    # # invocation case 4
    # with open('json_parser_tests/hardestFunctionCall.json') as file6:
    #     contents = json.load(file6)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG6 = functionList[length-1]
    # testCFG6.firstNode = addPreviousBlocks(testCFG6.firstNode)
    # printCFG(testCFG6.firstNode)
    # # dotToCFG(testCFG6.firstNode, "nested invocation case")


# UNSURE ABOUT THIS, SINCE THERE IS ONLY ONE BLOCK, THERE ISNT A GRAPH TO SHOW
    # # simple unary case 
    # with open('json_parser_tests/simpleUnary.json') as file7:
    #     contents = json.load(file7)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG7 = functionList[length-1]
    # testCFG7.firstNode = addPreviousBlocks(testCFG7.firstNode)
    # # printCFG(testCFG7.firstNode)
    # dotToCFG(testCFG7.firstNode, "simple unary case")


    # # lgtm
    # # invocation unary case 
    # with open('json_parser_tests/invocationUnary.json') as file8:
    #     contents = json.load(file8)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG8 = functionList[length-1]
    # testCFG8.firstNode = addPreviousBlocks(testCFG8.firstNode)
    # # printCFG(testCFG8.firstNode)
    # dotToCFG(testCFG8.firstNode, "invocation unary case")

# same as above ^ - UNSURE ABOUT THIS, SINCE THERE IS ONLY ONE BLOCK, THERE ISNT A GRAPH TO SHOW
    # simple binop case
    with open('json_parser_tests/simpleBinop.json') as file9:
        contents = json.load(file9)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG9 = functionList[length-1]
    testCFG9.firstNode = addPreviousBlocks(testCFG9.firstNode)
    # printCFG(testCFG9.firstNode)
    dotToCFG(testCFG9.firstNode, "simple binop case")


    # # invocation binop case 
    # with open('json_parser_tests/invocationBinop.json') as file10:
    #     contents = json.load(file10)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG10 = functionList[length-1]
    # testCFG10.firstNode = addPreviousBlocks(testCFG10.firstNode)
    # # printCFG(testCFG10.firstNode)
    # dotToCFG(testCFG10.firstNode, "invocation binop case")

    # # lgtm
    # # nested if case
    # with open('json_parser_tests/nested_if.json') as file11:
    #     contents = json.load(file11)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG11 = functionList[length-1]
    # testCFG11.firstNode = addPreviousBlocks(testCFG11.firstNode)
    # # printCFG(testCFG11.firstNode)
    # dotToCFG(testCFG11.firstNode, "nested if case")

    # # lgtm
    # # nested else case
    # with open('json_parser_tests/nested_else.json') as file12:
    #     contents = json.load(file12)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # testCFG12 = functionList[length-1]
    # testCFG12.firstNode = addPreviousBlocks(testCFG12.firstNode)
    # # printCFG(testCFG12.firstNode)
    # dotToCFG(testCFG12.firstNode, "nested else case")

    # # lgtm
    # # nested while case
    # with open('json_parser_tests/nested_while.json') as file13:
    #     contents = json.load(file13)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG13 = functionList[length-1]
    # testCFG13.firstNode = addPreviousBlocks(testCFG13.firstNode)
    # # printCFG(testCFG13.firstNode)
    # dotToCFG(testCFG13.firstNode, "nested while case")


    # lgtm
    # if while nested case
    # with open('json_parser_tests/if_while_nested.json') as file14:
    #     contents = json.load(file14)
    # ast = parse(contents)
    # functionList = tmp(ast)
    # # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG14 = functionList[length-1]
    # testCFG14.firstNode = addPreviousBlocks(testCFG14.firstNode)
    # printCFG(testCFG14.firstNode)
    # dotToCFG(testCFG14.firstNode, "if while nested case")


    # # lgtm
    # # while if nested case
    # with open('json_parser_tests/while_if_nested.json') as file15:
    #     contents = json.load(file15)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG15 = functionList[length-1]
    # testCFG15.firstNode = addPreviousBlocks(testCFG15.firstNode)
    # # printCFG(testCFG15.firstNode)
    # dotToCFG(testCFG15.firstNode, "while if nested case")


    # # lgtm
    # # triple nested if case
    # with open('json_parser_tests/if_triple_nest.json') as file16:
    #     contents = json.load(file16)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # length = len(functionList)
    # testCFG16 = functionList[length-1]
    # testCFG16.firstNode = addPreviousBlocks(testCFG16.firstNode)
    # # printCFG(testCFG16.firstNode)
    # dotToCFG(testCFG16.firstNode, "triple nested if case")


    # # lgtm
    # # triple nested while case
    # with open('json_parser_tests/while_triple_nest.json') as file17:
    #     contents = json.load(file17)
    # ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    # # print(str(functionList))
    # length = len(functionList)
    # testCFG17 = functionList[length - 1]
    # testCFG17.firstNode = addPreviousBlocks(testCFG17.firstNode)
    # printCFG(testCFG17.firstNode)
    # # dotToCFG(testCFG17.firstNode, "nested while case")







    for func in functionList:
        print("\ncurrent function: " + str(func.firstNode.id) + "\n")

        queue = []
        queue.append(func.firstNode)
        nodeDict = {}

        while queue != []:
            currNode = queue.pop(0)

            if currNode in nodeDict:
                continue

            print("\nnew block\n")

            nodeDict[currNode] = True

            for codeLine in currNode.code:
                print(codeLine + "\n")

            for nextNode in currNode.nextBlocks:
                queue.append(nextNode)




if __name__ == "__main__":
    main()