import unittest
from ast_class_definitions import *
from cfg_generator import *
from json_parser import *
from generateLLVM import *
import test_ast_trees
import json
import os
import copy
from ssaGenerator import *

# NOTE: YOU WILL WANT TO HAVE A NODE AT THE START OF THE CFG FOR INITIALIZATION PURPOSES LATER

# YOU WILL NEED  A WAY TO PASS ALONG ALL OF THE FUNCTIONS HEAD NODES IN A LIST SO THAT THEY ARE EASY TO GRAB

# FOR EACH ONE YOU WILL NEED TO CREATE A MAPPING FOR EACH PARAMETER OF THE FUNCTION



# step through the node tree and print a formatted dot file
def dotToCFG(head, name):




# HERE I NEED TO WRITE CODE THAT WILL ADD CODE FROM EACH NODE INTO ITS RESPECTIVE CFG NODE.
# IF IM NOT MISTAKEN, THE CODE WILL ALREADY BE IN SSA-LLVM WHEN THIS FUNCTION IS CALLED.
# MAY NEED TO REFERENCE RESPECTIVE NOTES TO REMEMBER HOW THIS SHOULD BE FORMATTED




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
            print("  " + str(currNode.id) + " -> " + str(node.id) + ";")
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
            # add the current node to the previousBlocks list
            if curr not in node.previousBlocks:
                node.previousBlocks.append(curr)

            if node not in visitedDict:
                queue.append(node)

    return head



# add an empty block at the start and end of each while as well as the start and end of each if/if-else
# also add a return block for stack cleanup - all returns will point to this one cleanup point
# finally add an initial block that goes before the head
# return the new updated head
def addEmptyBlocks(head):
    emptyBlockId = -1

    queue = [head]      # kick off the queue with the intial head
    nodeDict = {}       # tracks when a node has been visited
    idCodeDict = {}     # tracks the inital idCode of each node


    # step through every node in the tree
    while queue != []:
        currNode = queue.pop(0)

        # track the initial idCode of each node (we will need to restore this later
        if currNode.id not in idCodeDict:
            idCodeDict[currNode.id] = copy.deepcopy(currNode.idCode)

        if currNode in nodeDict:
            continue


        # if convergence block case (code 2)
        if currNode.idCode is not None and 2 in currNode.idCode:
            # print("entered if convergence")

            currNode.idCode.remove(2)

            newPrevNode = CFG_Node(-1, [], [], [], emptyBlockId)
            emptyBlockId -= 1

            newPrevNode.nextBlocks = [currNode]

            # update all the previous blocks
            for tempNode in currNode.previousBlocks:
                newPrevNode.previousBlocks.append(tempNode)
                tempNode.nextBlocks.remove(currNode)
                tempNode.nextBlocks.append(newPrevNode)

            currNode.previousBlocks = [newPrevNode]

            # throw back onto the queue in case it is also a while or if guard
            queue.append(currNode)

            # since we can have a convergence block (2) and a while (3) or if guard (1), we dont put this into the dict
            continue



        # while guard block case (code 3)
        elif currNode.idCode is not None and 3 in currNode.idCode:
            currNode.idCode.remove(3)

            newPrevNode = CFG_Node(-1, [], [], [], emptyBlockId)
            newPrevNode.nextBlocks = [currNode]
            emptyBlockId -= 1

            newNextNode = CFG_Node(-1, [], [], [], emptyBlockId)
            newNextNode.previousBlocks = [currNode]
            emptyBlockId -= 1

            # fix up the previous and next block lists for both temp node and the new node
            for tempNode in currNode.previousBlocks:
                # need to recoginize which is the return from the while body
                # since the id is less, this must NOT be the return from body
                if tempNode.id < currNode.id:
                    newPrevNode.previousBlocks.append(tempNode)
                    tempNode.nextBlocks.remove(currNode)
                    tempNode.nextBlocks.append(newPrevNode)

                # this must be the return from while body
                else:
                    currNode.previousBlocks = [tempNode]

            currNode.previousBlocks.append(newPrevNode)

            # want to put the new next between the guard and node that isnt the body
            for tempNode in currNode.nextBlocks:
                # this is NOT the body
                if tempNode.idCode == None or 4 not in tempNode.idCode:
                    # print("guard to next (not body)")
                    newNextNode.nextBlocks.append(tempNode)
                    tempNode.previousBlocks.remove(currNode)
                    tempNode.previousBlocks.append(newNextNode)

                # this is the body
                else:
                    currNode.nextBlocks = [tempNode]

            currNode.nextBlocks.append(newNextNode)



        # if guard block case (code 1) - this encompasses if-else and just plain if
        elif currNode.idCode is not None and 1 in currNode.idCode:
            currNode.idCode.remove(1)

            newPrevNode = CFG_Node(-1, [], [], [], emptyBlockId)
            emptyBlockId -= 1

            newPrevNode.nextBlocks = [currNode]

            # update all of the previous blocks
            for tempNode in currNode.previousBlocks:
                newPrevNode.previousBlocks.append(tempNode)
                tempNode.nextBlocks = [newPrevNode]

            currNode.previousBlocks.append(newPrevNode)




        # just a regular block, this is just here in case you decide to add something later
        else:
            pass

        # update the dict entry
        nodeDict[currNode] = True

        # enqueue all of the next nodes
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)



    # now we restore the idCode for each node
    queue = [head]  # kick off the queue with the intial head
    nodeDict = {}  # tracks when a node has been visited

    # step through every node in the tree
    while queue != []:
        currNode = queue.pop(0)

        # restore the idCode field of each node using the dictionary from before
        if currNode.id in idCodeDict:
            currNode.idCode = idCodeDict[currNode.id]

        if currNode in nodeDict:
            continue
        else:
            # update the dict entry
            nodeDict[currNode] = True

        # enqueue all of the next nodes
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)



    queue = [head]
    nodeDict = {}

    returnLinkNode = CFG_Node(-1, [], [], [], emptyBlockId) # NO IDEA WHAT I SHOULD PUT IN THE LAST USED REGISTER FIELD
    emptyBlockId -= 1

    # walk back thru and for each return block add a next block that goes to the same place
    while queue != []:
        currNode = queue.pop(0)

        # check if youve already looked at the currnode
        if currNode in nodeDict:
            continue
        else:
            nodeDict[currNode] = True

        # add all the next blocks to the queue
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)

        # for each node you will step through the lines of code
        for line in currNode.code:
            # if a line of code is an m_ret, link the currNode to the only return block
            # we link ONLY to the return block. Remove all other nextBlock links
            matchVar = line.split()
            if len(matchVar) < 1:
                continue

            match matchVar[0]:
                case "ret":
                    # link the curr node to the return node
                    currNode.nextBlocks = [returnLinkNode]
                    # add the curr node to the return node previous list
                    returnLinkNode.previousBlocks.append(currNode) # THIS MAY NOT BE NECESSARY
                    break

                # just continue to the next node
                case _:
                    continue


    # finally add an initial block at the start that is empty
    initialBlock = CFG_Node(-1, [], [], [], emptyBlockId) # NO IDEA WHAT I SHOULD PUT IN THE LAST USED REGISTER FIELD
    emptyBlockId -= 1
    initialBlock.nextBlocks = [head]

    # make initial block the actual initial block
    head.previousBlocks = [initialBlock]

    # return the initial block as if its the head
    return initialBlock



# step through each node and print the head
def printCFG(head):
    print("-----------------------------------\nEntered Print Function\n-----------------------------------\n")
    nodeNum = 0
    nodeLevel = 0

    queue = []

    nodeReferences = {}

    queue.append( (head, nodeLevel) )

    while queue != []:
        currTuple = queue.pop(0)
        currNode = currTuple[0]

        if nodeLevel <= currTuple[1]:
            nodeLevel += 1


        # if str(currNode.code) not in nodeReferences:
        if str(currNode.id) not in nodeReferences:
            nodeReferences[str(currNode.id)] = 1

            for node in currNode.nextBlocks:
                queue.append( (node, nodeLevel + 1) )


        else:
            nodeReferences[str(currNode.id)] = nodeReferences[str(currNode.id)] + 1
            continue

        print(currNode.code)

        for node in currNode.nextBlocks:
            print("nextNode id: " + str(node.id))

        for node in currNode.previousBlocks:
            print("prevNode id: " + str(node.id))

        print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.id)]) + "\nblock Id: " + str(currNode.id) + "\nblock idCodes: " + str(currNode.idCode) + "\n\n\n")
        nodeNum += 1




# dotFlag tells us if we should print the node or output the .dot file
# simple function case
def testa(dotFlag):  # if dotFlag == True, print the dot output instead of print
    functionList = tmp(test_ast_trees.expected3)
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected3)
    length = len(functionList)
    testCFGa = functionList[length - 1]
    if(dotFlag):
        dotToCFG(testCFGa.firstNode, "trivial case")
    else:
        printCFG(testCFGa.firstNode)



# invocation case
def testb(dotFlag):
    functionList = tmp(test_ast_trees.expected7)
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected7)
    length = len(functionList)
    testCFGb = functionList[length - 1]
    if(dotFlag):
        dotToCFG(testCFGb.firstNode, "simple invocation case")
    else:
        printCFG(testCFGb.firstNode)



# if case => if.mini
def testc(dotFlag):
    functionList = tmp(test_ast_trees.expected5)
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected5)
    length = len(functionList)
    testCFGc = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFGc.firstNode, "simple if case")
    else:
        printCFG(testCFGc.firstNode)



# while case => loop.mini
def test0(dotFlag):
    with open('json_parser_tests/loop.json') as file1:
        contents = json.load(file1)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(test_ast_trees.expected4)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG0 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG0.firstNode, "simple while case")
    else:
        printCFG(testCFG0.firstNode)



# simplest case of if else, print statement in each
def test1(dotFlag):
    with open('json_parser_tests/ifelse.json') as file1:
        contents = json.load(file1)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG1 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG1.firstNode, "simple if else case")
    else:
        printCFG(testCFG1.firstNode)
    print(testCFG1.ssaCode)



# while and then if-else case
def test2(dotFlag):
    with open('json_parser_tests/loop_if.json') as file2:
        contents = json.load(file2)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG2 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG2.firstNode, "while and then if-else case")
    else:
        printCFG(testCFG2.firstNode)



# if and then while loop case
def test3(dotFlag):
    with open('json_parser_tests/if_loop.json') as file3:
        contents = json.load(file3)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG3 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG3.firstNode, "if and then while loop case")
    else:
        printCFG(testCFG3.firstNode)




# invocation case 2
def test4(dotFlag):
    with open('json_parser_tests/myFunctionCall.json') as file4:
        contents = json.load(file4)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG4 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG4.firstNode, "simple invocation case")
    else:
        printCFG(testCFG4.firstNode)



# invocation case 3
def test5(dotFlag):
    with open('json_parser_tests/harderFunctionCall.json') as file5:
        contents = json.load(file5)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG5 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG5.firstNode, "two invocation case")
    else:
        printCFG(testCFG5.firstNode)



# invocation case 4
def test6(dotFlag):
    with open('json_parser_tests/hardestFunctionCall.json') as file6:
        contents = json.load(file6)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG6 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG6.firstNode, "nested invocation case")
    else:
        printCFG(testCFG6.firstNode)



# simple unary case
def test7(dotFlag):
    with open('json_parser_tests/simpleUnary.json') as file7:
        contents = json.load(file7)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG7 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG7.firstNode, "simple unary case")
    else:
        printCFG(testCFG7.firstNode)



# invocation unary case
def test8(dotFlag):
    with open('json_parser_tests/invocationUnary.json') as file8:
        contents = json.load(file8)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG8 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG8.firstNode, "invocation unary case")
    else:
        printCFG(testCFG8.firstNode)


# simple binop case
def test9(dotFlag):
    with open('json_parser_tests/simpleBinop.json') as file9:
        contents = json.load(file9)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG9 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG9.firstNode, "simple binop case")
    else:
        printCFG(testCFG9.firstNode)



# invocation binop case
def test10(dotFlag):
    with open('json_parser_tests/invocationBinop.json') as file10:
        contents = json.load(file10)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG10 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG10.firstNode, "invocation binop case")
    else:
        printCFG(testCFG10.firstNode)



# nested if case
def test11(dotFlag):
    with open('json_parser_tests/nested_if.json') as file11:
        contents = json.load(file11)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG11 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG11.firstNode, "nested if case")
    else:
        printCFG(testCFG11.firstNode)



# nested else case
def test12(dotFlag):
    with open('json_parser_tests/nested_else.json') as file12:
        contents = json.load(file12)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG12 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG12.firstNode, "nested else case")
    else:
        printCFG(testCFG12.firstNode)



# nested while case
def test13(dotFlag):
    with open('json_parser_tests/nested_while.json') as file13:
        contents = json.load(file13)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG13 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG13.firstNode, "nested while case")
    else:
        printCFG(testCFG13.firstNode)



# if while nested case
def test14(dotFlag):
    with open('json_parser_tests/if_while_nested.json') as file14:
        contents = json.load(file14)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG14 = functionList[length - 1]
    if(dotFlag):
        dotToCFG(testCFG14.firstNode, "if while nested case")
    else:
        printCFG(testCFG14.firstNode)



# while if nested case
def test15(dotFlag):
    with open('json_parser_tests/while_if_nested.json') as file15:
        contents = json.load(file15)
    ast = parse(contents)
    functionList = tmp(ast)
    # functionList = generate_CFG_Prog_Handler(ast)
    length = len(functionList)
    testCFG15 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG15.firstNode, "while if nested case")
    else:
        printCFG(testCFG15.firstNode)



# triple nested if case
def test16(dotFlag):
    with open('json_parser_tests/if_triple_nest.json') as file16:
        contents = json.load(file16)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG16 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG16.firstNode, "triple nested if case")
    else:
        printCFG(testCFG16.firstNode)



# triple nested while case
def test17(dotFlag):
    with open('json_parser_tests/while_triple_nest.json') as file17:
        contents = json.load(file17)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG17 = functionList[length - 1]
    if(dotFlag):
        dotToCFG(testCFG17.firstNode, "nested while case")
    else:
        printCFG(testCFG17.firstNode)



# simple if (no else) case
def test18(dotFlag):
    with open('json_parser_tests/if_no_else.json') as file18:
        contents = json.load(file18)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG18 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG18.firstNode, "simple if (no else) case")
    else:
        printCFG(testCFG18.firstNode)



# HAS AN EXTRA EMPTY BLOCK (node #6 and #9) seems pretty harmless tho
# triple nested if (no else) case
def test19(dotFlag):
    with open('json_parser_tests/nested_if_no_else.json') as file19:
        contents = json.load(file19)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG19 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG19.firstNode, "triple nested if (no else) case")
    else:
        printCFG(testCFG19.firstNode)



# 2 return case
def test20(dotFlag):
    with open('json_parser_tests/2_return.json') as file20:
        contents = json.load(file20)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG20 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG20.firstNode, "2 return case")
    else:
        printCFG(testCFG20.firstNode)



# 3 return (while) case
def test21(dotFlag):
    with open('json_parser_tests/3_return_while.json') as file21:
        contents = json.load(file21)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG21 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG21.firstNode, "3 return (while) case")
    else:
        printCFG(testCFG21.firstNode)



# HAS AN EXTRA EMPTY BLOCK (node #8) seems pretty harmless tho
# 3 return (if) case
def test22(dotFlag):
    with open('json_parser_tests/3_return_if.json') as file22:
        contents = json.load(file22)
    ast = parse(contents)
    # functionList = generate_CFG_Prog_Handler(ast)
    functionList = tmp(ast)
    length = len(functionList)
    testCFG22 = functionList[length-1]
    if(dotFlag):
        dotToCFG(testCFG22.firstNode, "3 return (if) case")
    else:
        printCFG(testCFG22.firstNode)





def main():
    # NOTE: when calling a test function:
        # False means print nodes:
            # test1(False)
        # True means print .dot file output:
            # test1(True)


    test1(False)



    # # loop for printing out the code from each function
    # for func in functionList:
    #     print("\ncurrent function: " + str(func.firstNode.id) + "\n")
    #
    #     queue = []
    #     queue.append(func.firstNode)
    #     nodeDict = {}
    #
    #     while queue != []:
    #         currNode = queue.pop(0)
    #
    #         if currNode in nodeDict:
    #             continue
    #
    #         print("\nnew block\n")
    #
    #         nodeDict[currNode] = True
    #
    #         for codeLine in currNode.code:
    #             print(codeLine + "\n")
    #
    #         for nextNode in currNode.nextBlocks:
    #             queue.append(nextNode)



if __name__ == "__main__":
    main()