import unittest
from ast_class_definitions import *
from cfg_generator import *
from json_parser import *
from generateLLVM import *
import test_ast_trees
import json
import os

# NOTE: YOU WILL WANT TO HAVE A NODE AT THE START OF THE CFG FOR INITIALIZATION PURPOSES LATER

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

        # WAS IN
        # for node in currNode.previousBlocks:
        #     print("prevNode id: " + str(node.id))

        print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.id)]) + "\nblock Id: " + str(currNode.id) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) + "\nnumReferences: " + str(nodeReferences[str(currNode.code)]) + "\n\n\n")
        # print("nodeNum: " + str(nodeNum) + "\nnodeLevel: " + str(currTuple[1]) +       "\n\n\n")# + "\nnumReferences: " + str(nodeReferences[nodeNum]) + "\n\n\n")
        
        nodeNum += 1


def main():
    # # simple function case
    # testCFGa = generate_CFG_Prog_Handler(test_ast_trees.expected3)
    # # printCFG(testCFGa.firstNode)
    # dotToCFG(testCFGa.firstNode, "trivial case")


    # # invocation case
    # testCFGb = generate_CFG_Prog_Handler(test_ast_trees.expected7)
    # # printCFG(testCFGb.firstNode)
    # dotToCFG(testCFGb.firstNode, "simple invocation case")


    # # if case => if.mini
    # testCFGc = generate_CFG_Prog_Handler(test_ast_trees.expected5)
    # # printCFG(testCFGc.firstNode)
    # dotToCFG(testCFGc.firstNode, "simple if case")
    

    # # good for now, may think more about functions that have no return statement later on
    # # while case => loop.mini
    # testCFG0 = generate_CFG_Prog_Handler(test_ast_trees.expected4)
    # # printCFG(testCFG0.firstNode)
    # dotToCFG(testCFG0.firstNode, "simple while case")


    # # simplest case of if else, print statement in each
    # with open('json_parser_tests/ifelse.json') as file1:
    #     contents = json.load(file1)
    # ast = parse(contents)
    # testCFG1 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG1.firstNode)
    # dotToCFG(testCFG1.firstNode, "simple if else case")

    # # lgtm
    # # while and then if-else case
    # with open('json_parser_tests/loop_if.json') as file2:
    #     contents = json.load(file2)
    # ast = parse(contents)
    # testCFG2 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG2.firstNode)
    # dotToCFG(testCFG2.firstNode, "while and then if-else case")


    # # lgtm
    # # if and then while loop case
    # with open('json_parser_tests/if_loop.json') as file3:
    #     contents = json.load(file3)
    # ast = parse(contents)
    # testCFG3 = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG3.firstNode)
    # # dotToCFG(testCFG3.firstNode, "if and then while loop case")


    # # looks good
    # # invocation case 2
    # with open('json_parser_tests/myFunctionCall.json') as file4:
    #     contents = json.load(file4)
    # ast = parse(contents)
    # testCFG4 = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG4.firstNode)
    # # dotToCFG(testCFG4.firstNode, "simple invocation case")


    # # looks good
    # # invocation case 3
    # with open('json_parser_tests/harderFunctionCall.json') as file5:
    #     contents = json.load(file5)
    # ast = parse(contents)
    # testCFG5 = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG5.firstNode)
    # # dotToCFG(testCFG5.firstNode, "two invocation case")


    # # lgtm
    # # invocation case 4
    # with open('json_parser_tests/hardestFunctionCall.json') as file6:
    #     contents = json.load(file6)
    # ast = parse(contents)
    # testCFG6 = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG6.firstNode)
    # # dotToCFG(testCFG6.firstNode, "nested invocation case")


# UNSURE ABOUT THIS, SINCE THERE IS ONLY ONE BLOCK, THERE ISNT A GRAPH TO SHOW
    # # simple unary case 
    # with open('json_parser_tests/simpleUnary.json') as file7:
    #     contents = json.load(file7)
    # ast = parse(contents)
    # testCFG7 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG7.firstNode)
    # dotToCFG(testCFG7.firstNode, "simple unary case")


    # # lgtm
    # # invocation unary case 
    # with open('json_parser_tests/invocationUnary.json') as file8:
    #     contents = json.load(file8)
    # ast = parse(contents)
    # testCFG8 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG8.firstNode)
    # dotToCFG(testCFG8.firstNode, "invocation unary case")

# same as above ^ - UNSURE ABOUT THIS, SINCE THERE IS ONLY ONE BLOCK, THERE ISNT A GRAPH TO SHOW
    # # simple binop case 
    # with open('json_parser_tests/simpleBinop.json') as file9:
    #     contents = json.load(file9)
    # ast = parse(contents)
    # testCFG9 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG9.firstNode)
    # dotToCFG(testCFG9.firstNode, "simple binop case")


    # # invocation binop case 
    # with open('json_parser_tests/invocationBinop.json') as file10:
    #     contents = json.load(file10)
    # ast = parse(contents)
    # testCFG10 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG10.firstNode)
    # dotToCFG(testCFG10.firstNode, "invocation binop case")

    # # lgtm
    # # nested if case
    # with open('json_parser_tests/nested_if.json') as file11:
    #     contents = json.load(file11)
    # ast = parse(contents)
    # testCFG11 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG11.firstNode)
    # dotToCFG(testCFG11.firstNode, "nested if case")

    # # lgtm
    # # nested else case
    # with open('json_parser_tests/nested_else.json') as file12:
    #     contents = json.load(file12)
    # ast = parse(contents)
    # testCFG12 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG12.firstNode)
    # dotToCFG(testCFG12.firstNode, "nested else case")

    # # lgtm
    # # nested while case
    # with open('json_parser_tests/nested_while.json') as file13:
    #     contents = json.load(file13)
    # ast = parse(contents)
    # testCFG13 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG13.firstNode)
    # dotToCFG(testCFG13.firstNode, "nested while case")


    # # lgtm
    # # if while nested case
    # with open('json_parser_tests/if_while_nested.json') as file14:
    #     contents = json.load(file14)
    # ast = parse(contents)
    # testCFG14 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG14.firstNode)
    # dotToCFG(testCFG14.firstNode, "if while nested case")


    # # not good
    # # while if nested case
    # with open('json_parser_tests/while_if_nested.json') as file15:
    #     contents = json.load(file15)
    # ast = parse(contents)
    # testCFG15 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG15.firstNode)
    # dotToCFG(testCFG15.firstNode, "while if nested case")


    # # lgtm
    # # triple nested if case
    # with open('json_parser_tests/if_triple_nest.json') as file16:
    #     contents = json.load(file16)
    # ast = parse(contents)
    # testCFG16 = generate_CFG_Prog_Handler(ast)
    # # printCFG(testCFG16.firstNode)
    # dotToCFG(testCFG16.firstNode, "triple nested if case")


    # not good
    # triple nested while case
    with open('json_parser_tests/while_triple_nest.json') as file17:
        contents = json.load(file17)
    ast = parse(contents)
    testCFG17 = generate_CFG_Prog_Handler(ast)
    printCFG(testCFG17.firstNode)
    # dotToCFG(testCFG17.firstNode, "nested while case")


if __name__ == "__main__":
    main()