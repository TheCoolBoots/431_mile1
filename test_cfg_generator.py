import unittest
from ast_class_definitions import *
from cfg_generator import *
from json_parser import *
import test_ast_trees
import json



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
    # # simple case
    # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected3)
    # printCFG(testCFG.firstNode)

    # # invocation case
    # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected7)
    # printCFG(testCFG.firstNode)


    # # if case
    # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected5)
    # printCFG(testCFG.firstNode)
    

    # while case 
    # testCFG = generate_CFG_Prog_Handler(test_ast_trees.expected4)
    # printCFG(testCFG.firstNode)


    # with open('json_parser_tests/ifelse.json') as file1:
    #     contents = json.load(file1)
    # ast = parse(contents)
    # testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)


    # while and then if-else case
    # with open('json_parser_tests/loop_if.json') as file2:
    #     contents = json.load(file2)
    # ast = parse(contents)
    # # THIS SHOULDNT BE ELSE, IT SEEMS THAT THE ELSE STATEMENTS ARENT BEING PARSED
    # # dont consider the else case on line 77 of json_parse.py
    # # print("\n\n\n\n" + str(ast.functions[0].statements[1].else_statements) + "\n\n\n\n")
    # # print("\n\n\ln\nHERE" + str(ast.functions[0].statements[2].else_statements) + "HERE\n\n\n\n")
    # testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)



    # with open('json_parser_tests/if_loop.json') as file3:
    #     contents = json.load(file3)
    # ast = parse(contents)
    # # THIS SHOULDNT BE ELSE, IT SEEMS THAT THE ELSE STATEMENTS ARENT BEING PARSED
    # # dont consider the else case on line 77 of json_parse.py
    # # print("\n\n\n\n" + str(ast.functions[0].statements[1].else_statements) + "\n\n\n\n")
    # # print("\n\n\ln\nHERE" + str(ast.functions[0].statements[2].else_statements) + "HERE\n\n\n\n")
    # testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)


    # invocation case 2
    with open('json_parser_tests/myFunctionCall.json') as file4:
        contents = json.load(file4)
    ast = parse(contents)
    testCFG = generate_CFG_Prog_Handler(ast)
    printCFG(testCFG.firstNode)


    # # invocation case 3
    # with open('json_parser_tests/harderFunctionCall.json') as file5:
    #     contents = json.load(file5)
    # ast = parse(contents)
    # testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)


    # # invocation case 4
    # with open('json_parser_tests/hardestFunctionCall.json') as file6:
    #     contents = json.load(file6)
    # ast = parse(contents)
    # testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)

if __name__ == "__main__":
    main()