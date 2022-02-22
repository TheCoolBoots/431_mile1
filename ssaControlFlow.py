from typing import Dict, Tuple
from ast_class_definitions import *
from cfg_generator import *
from ssaGenerator import generateSSA
from ssaGenerator import expressionToSSA
import copy


def astToSSA(prog:m_prog) -> list[CFG_Node]:
    # create a function node for each function
    functionList = generate_CFG_Prog_Handler(prog) # this is a list of function nodes

    # printCFG(functionList[len(functionList) - 1].firstNode)

    # generate globals, generate top_env, generate types
    lastReg = 0
    globalDeclarations = []
    for dec in prog.global_declarations:
        # get the list of code from the current declaration
        declarationList = dec.getSSAGlobals()

        # extend the globalDeclarations list of code
        globalDeclarations.extend(declarationList)

    # getTopEnv(self, includeLineNum=True)
    # get the dictionary of string to type in the global environment
    globalTopEnv = prog.getTopEnv(False)

    globalReg = lastReg

    # will need to step through each statement in each block in each function
    for fun in functionList:
        lastReg = globalReg
        currBlock = fun.firstNode # get the first block in a function

        # make dict of traversed nodes
        nodeDict = {}

        # make queue for traversing nodes
        queue = []

        # start off the queue
        queue.append(currBlock)

        # step through each block of current tree and convert statements to SSA LLVM
        while queue != []:
            # take first item from the queue
            currBlock = queue.pop(0)

            # check if youve already looked at this node
            if currBlock in nodeDict:
                continue

            currBlock.lastRegUsed = lastReg

            # add the current node to the visited dict
            nodeDict[currBlock] = True

            # will need to include global environment in the generateSSA function
            # _generateSSA(currentNode: CFG_Node, types, functions) : return code, currentNode.mappings

            # this is a guard node
            if(IdCodes.IF_GUARD in currBlock.idCode or IdCodes.WHILE_GUARD in currBlock.idCode):
                # lastReg, tempCode, mappings = generateSSA(currBlock, globalTopEnv, prog.getTypes(), generateFunctionTypes(prog))
                lastReg, garbage, tempCode = expressionToSSA(lastReg, globalTopEnv, prog.getTypes(), generateFunctionTypes(prog), currBlock)

            else:
                lastReg, tempCode, mappings = generateSSA(currBlock, globalTopEnv, prog.getTypes(), generateFunctionTypes(prog)) # _generateSSA(currBlock, prog.getTypes(), generateFunctionTypes(prog), globalTopEnv)


            # update the ast code to be replaced with SSA LLVM code
            currBlock.code = tempCode

            # '\n'.join(codeList) # takes every element in the list and puts \n between them (turns into one string)

            currBlock.mappings = mappings # YES?

            # check if there are any next nodes, add them if so
            for tempNode in currBlock.nextBlocks:
                queue.append(tempNode)

    # add the empty and previous blocks for each function
    length = len(functionList)
    i = 0
    while i < length:
        functionList[i].firstNode = addPreviousBlocks(functionList[i].firstNode)
        functionList[i].firstNode = addEmptyBlocks(functionList[i].firstNode)
        i += 1

    # function will return a string of code that has the while and if statements incorperated
    # codeList = []
    length = len(functionList)
    i = 0
    while i < length:
        currSSACode = branchesToSSA(functionList[i].firstNode)
        # codeList.append(ssaCode)
        functionList[i].ssaCode = currSSACode
        i += 1

    return functionList


# compiles if and while structures into SSA code
# body statements are already compiled and stored inside CFG_Node.code
# returns list of llvm SSA instructions that includes body statements
def branchesToSSA(head:CFG_Node) -> list[str]:
    nodeDict = {}               # make dict of traversed nodes
    queue = []                  # make queue for traversing nodes
    queue.append(head)          # start off the queue
    currCode = ""               # this is the code from the current function

    # step through each block of current tree and find the if and while statements
    while queue != []:
        currNode = queue.pop(0)    # take first item from the queue

        # check if youve already looked at this node
        if currNode in nodeDict:
            continue

        # # add the current node to the visited dict
        # nodeDict[currNode] = True

        # if guard block case (code 1) - this encompasses if-else and just plain if
        if currNode.idCode is not None and 1 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # may want to check if you have an else block first
            elseFlag = 1  # 1 indicates that there IS an else block
            ifBlock = None  # ifBlock initially None
            elseBlock = None  # elseBlock initially None
            for tempNode in currNode.nextBlocks:
                # this is the convergence, there is no else
                if tempNode.idCode != None and 2 in tempNode.idCode:
                    elseFlag = 0  # 0 indicates no else

                # save the if block for later (this will catch if and else blocks if they both exist)
                else:
                    # IMPORTANT: We are assuming that the if node comes before the else block (fairly certain this will always be true)
                    if ifBlock == None:
                        ifBlock = tempNode
                    # if there are two blocks, this will catch the else block
                    else:
                        elseBlock = tempNode

            # add code for if block start
            # evaluate guard expression
            # lastRegUsed, code, mappings = generateSSA(...)
            # currCode += code # "\nIF BLOCK START PLACEHOLDER {\n"
            currCode += "\nIF BLOCK START PLACEHOLDER {\n"

            # use the ifElseCodeHelper on the if statement
            # if statement has else block:
                # br i32 [guard reg], label %[lastRegUsed+1], label %[lastRegUsed+2]
                # lastRegUsed += 3
            # else:
                # br i32 [guard reg], label %[lastRegUsed+1], label %[lastRegUsed+2]
                # lastRegUsed += 2
            # add "{lastRegUsed+1}:" to code list (label)
            newTuple = ifElseCodeHelper(ifBlock, nodeDict)
            newCode = newTuple[0]
            convergenceNode = newTuple[1]  # this may be None if it ended in Return
            nodeDict = newTuple[2]

            # add the code to the currCode
            currCode += newCode

            # evaluate if block statements, add to code list
            # if statement has else block, add jump to label %{lastRegUsed+3
            #   if it doesnt, add jump to label %{lastRegUsed + 2}
            # add "{lastRegUsed+2}:" to code list ()
            
            currCode += "\nIF BLOCK END PLACEHOLDER }\n"

            # if there is an else block
            if elseFlag == 1:
                # add code for else block start
                currCode += "\nELSE BLOCK START PLACEHOLDER {\n"

                # use the ifElseCodeHelper on the else statement
                newTuple = ifElseCodeHelper(elseBlock, nodeDict)
                newCode = newTuple[0]

                # if the if block ended in a return, we will have a None here
                if convergenceNode == None:
                    convergenceNode = newTuple[1]  # technically this should be the same as above

                nodeDict = newTuple[2]

                # add the code to the currCode
                currCode += newCode

                # add code for else block end
                currCode += "\nELSE BLOCK END PLACEHOLDER }\n"
                # if statement has else block:
                    # evaluate else block statements and add to code list
                    # add jump to %{lastRegUsed+3}
                    # add "{lastRegUsed+3}:"

            # if there is no else block
            else:
                # add code for no else block ?
                currCode += "\nNO ELSE BLOCK PLACEHOLDER\n"
                # possibly need to link guard to not if somehow

            nodeDict[currNode] = True

            # it is possible that all paths ended in return
            if convergenceNode != None:
                queue.append(
                    convergenceNode)  # append the convergence node so that you will traverse it (we ignore the if branches we already searched)

            continue  # we don't add the currNode to the dict here since a convergence node can also be other things

        # while guard block case (code 3)
        elif currNode.idCode != None and 3 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # add the code for start of while: while (statement) {
                # what exactly does this look like in SSA-LLVM ??
            
            #evaluate guard statement, add code to codelist
            # reserve 3 register slots for labels (lastRegUsed+1, +2, +3)
            # add entry label {lastRegUsed + 1}
            # add branch instruction br i32 [guardreg], label %{lastRegUsed+2}, label %{lastRegUsed+3}
            currCode += "\nSTART OF WHILE (PLACEHOLDER STATEMENT) {\n"  # THIS IS OBVIOUSLY NOT CORRECT
            # add body entry label to codelist {lastRegUsed+2}:
            # evaluate while body statements and add code to codelist

            # NOTE: THIS IS ALSO WHERE WE CAN DEAL WITH THE m_bool, m_unary, m_binop IN THE GUARD STATEMENT
                # could also do it in _ssaGenerator if we want
                # expression to SSA for guard statements
                # THINK ABOUT GETTING LAST REGISTER USED FROM PREVIOUS NODE

            # traverse the while body using whileCodeHelper
            for tempNode in currNode.nextBlocks:
                # if you are looking at the body, traverse with whileCodeHelper
                if 4 in tempNode.idCode:

                    # THINKING I SHOULD PASS IN THE currNode and tempNode SO WE KNOW WHEN WE'VE REACHED THE ORIGINAL WHILE GUARD?
                    newTuple = whileCodeHelper(tempNode, currNode, nodeDict)
                    newCode = newTuple[0]
                    nodeDict = newTuple[1]

                    # add this new code to the currCode string
                    currCode += newCode

                # add the next (not body) node to the queue
                else:
                    queue.append(tempNode)

            # br %{lastRegUsed + 1}
            # add exit label {lastRegUsed+3}:

            # add the code for end of while: }
                # what exactly does this look like in SSA-LLVM ??
            currCode += "\nEND OF WHILE }\n"  # THIS IS OBVIOUSLY NOT CORRECT

            # add currNode to dict
            nodeDict[currNode] = True
            continue

        # body is typical (not an if or while component - could technically be a while body or if convergence but it shouldnt be)
        else:
            # shouldnt get an if convergence or while body here
            if currNode.idCode != None and (2 in currNode.idCode or 4 in currNode.idCode):
                print("\nWHY IS THIS HAPPENING\n\n")

            for currLine in currNode.code:
                currCode += currLine

        # check if there are any next nodes, add them if so
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)  # might want to pre-screen nodes before adding them to save some extra time

        # add currNode to the dictionary
        nodeDict[currNode] = True

    # this will be the code for each function (same order)
    return currCode


# idea is that the helper will walk through body node until it reaches:
    # the while guard
    # a dead end (likely the return block)
    # anything else?
# and then it will return the block of code that it generated
# what should we do if we reach another while? another if?

# returns llvm code between guardNode (inclusive) and exit node (exclusive), visited nodes
def whileCodeHelper(head:CFG_Node, guardNode:CFG_Node, nodeDict:dict) -> Tuple[list[str], dict]:
    # nodeDict = {}  # make dict of traversed nodes
    queue = []  # make queue for traversing nodes
    queue.append(head)  # start off the queue
    currCode = ""  # this is the code from the current function

    # step through each block of current tree and find the if and while statements
    while queue != []:
        currNode = queue.pop(0)  # take first item from the queue

        # check if youve already looked at this node
        if currNode in nodeDict:
            continue

        # if guard block case (code 1) - this encompasses if-else and just plain if
        if currNode.idCode is not None and 1 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # may want to check if you have an else block first
            elseFlag = 1  # 1 indicates that there IS an else block
            ifBlock = None  # ifBlock initially None
            elseBlock = None  # elseBlock initially None
            for tempNode in currNode.nextBlocks:
                # this is the convergence, there is no else
                if tempNode.idCode != None and 2 in tempNode.idCode:
                    elseFlag = 0  # 0 indicates no else

                # save the if block for later (this will catch if and else blocks if they both exist)
                else:
                    # IMPORTANT: We are assuming that the if node comes before the else block (fairly certain this will always be true)
                    if ifBlock == None:
                        ifBlock = tempNode
                    # if there are two blocks, this will catch the else block
                    else:
                        elseBlock = tempNode

            # add code for if block start
            currCode += "\nIF BLOCK START PLACEHOLDER {\n"

            # use the ifElseCodeHelper on the if statement
            newTuple = ifElseCodeHelper(ifBlock, nodeDict)
            newCode = newTuple[0]
            convergenceNode = newTuple[1]  # this may be None if it ended in Return
            nodeDict = newTuple[2]

            # add the code to the currCode
            currCode += newCode

            # add code for if block end
            currCode += "\nIF BLOCK END PLACEHOLDER }\n"

            # if there is an else block
            if elseFlag == 1:
                # add code for else block start
                currCode += "\nELSE BLOCK START PLACEHOLDER {\n"

                # use the ifElseCodeHelper on the else statement
                newTuple = ifElseCodeHelper(elseBlock, nodeDict)
                newCode = newTuple[0]

                # if the if block ended in a return, we will have a None here
                if convergenceNode == None:
                    convergenceNode = newTuple[1]  # technically this should be the same as above

                nodeDict = newTuple[2]

                # add the code to the currCode
                currCode += newCode

                # add code for else block end
                currCode += "\nELSE BLOCK END PLACEHOLDER }\n"

            # if there is no else block
            else:
                # add code for no else block ?
                currCode += "\nNO ELSE BLOCK PLACEHOLDER\n"
                # possibly need to link guard to not if somehow

            nodeDict[currNode] = True

            # it is possible that all paths ended in return
            if convergenceNode != None:
                queue.append(
                    convergenceNode)  # append the convergence node so that you will traverse it (we ignore the if branches we already searched)

            continue  # we don't add the currNode to the dict here since a convergence node can also be other things

        # while guard block case (code 3) - the one that you passed in
        elif currNode.idCode != None and 3 in currNode.idCode and currNode.id == guardNode.id:

            # anything we need to do here????

            # THIS IS AN IMPORTANT SPECIAL CASE WHERE YOU FIND THE ORIGINAL GUARD BLOCK.
            # YOU WILL RETURN BACK WITH ALL THE CODE YOU'VE ACCUMULATED SO THAT THE UPPER LEVEL FUNCTION CAN DEAL WITH IT.

            return (currCode, nodeDict)

        # while guard block case (code 3)
        elif currNode.idCode != None and 3 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # add the code for start of while: while (statement) {
                # what exactly does this look like in SSA-LLVM ??
            currCode += "\nSTART OF WHILE (PLACEHOLDER STATEMENT) {\n"  # THIS IS OBVIOUSLY NOT CORRECT

            # NOTE: THIS IS ALSO WHERE WE CAN DEAL WITH THE m_bool, m_unary, m_binop IN THE GUARD STATEMENT
                # could also do it in _ssaGenerator if we want

            # traverse the while body using whileCodeHelper
            for tempNode in currNode.nextBlocks:
                # if you are looking at the body, traverse with whileCodeHelper
                if 4 in tempNode.idCode:

                    # THINKING I SHOULD PASS IN THE currNode and tempNode SO WE KNOW WHEN WE'VE REACHED THE ORIGINAL WHILE GUARD?
                    newTuple = whileCodeHelper(tempNode, currNode, nodeDict)
                    newCode = newTuple[0]
                    nodeDict = newTuple[1]

                    # add this new code to the currCode string
                    currCode += newCode

                # add the next (not body) node to the queue
                else:
                    queue.append(tempNode)

            # add the code for end of while: }
                # what exactly does this look like in SSA-LLVM ??
            currCode += "\nEND OF WHILE }\n"  # THIS IS OBVIOUSLY NOT CORRECT

            # add currNode to dict
            nodeDict[currNode] = True

            continue

        # body is typical (not an if or while component)
        else:
            for currLine in currNode.code:
                currCode += currLine

        # check if there are any next nodes, add them if so
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)

        # add the current node to the visited dict
        nodeDict[currNode] = True

    # this return signifies that we finished the queue without finding the original while guard (reached a return statement)
    return currCode, nodeDict


# step thru the if/else nodes until you find a convergence block, another if guard, another while guard, or a dead end (return)
# each of these is a special case
# ONE MAIN DIFFERENCE FROM A WHILE STATEMENT IS THAT YOU MAY NEED TO RETURN THE CONVERGENCE BLOCK SO THAT YOU CAN CONTINUE WALKING THE NODES

# returns llvm code of one branch of an if statement, convergence node, nodes visited dict
def ifElseCodeHelper(head:CFG_Node, nodeDict:dict) -> Tuple[list[str], CFG_Node, dict]:
    # nodeDict = {}  # make dict of traversed nodes
    queue = []  # make queue for traversing nodes
    queue.append(head)  # start off the queue
    currCode = ""  # this is the code from the current function

    # step through each block of current tree and find the if and while statements
    while queue != []:
        currNode = queue.pop(0)  # take first item from the queue

        # check if youve already looked at this node
        if currNode in nodeDict:
            continue

        # # add the current node to the visited dict
        # nodeDict[currNode] = True

        # if convergence block case (code 2)
        if currNode.idCode is not None and 2 in currNode.idCode:

            # SPECIAL CASE!
            # YOU FOUND THE CONVERGENCE BLOCK, THIS MEANS THAT YOU CAN RETURN THE CODE YOU HAVE SO FAR
            # YOU SHOULD PROBABLY RETURN THIS NODE (along with the accumulated code) SO THAT YOU CAN CONTINUE WALKING THE NODES
            # IMPORTANT NOTE! DONT ADD THE CODE FROM THIS TO YOUR CODE FIELD.
            # YOU WILL WANT TO DO THAT IN THE HIGHER LEVEL FUNCTION.

            # We remove the code so that if this is a doubly nested call, the convergence node doesnt confuse us.
            currNode.idCode.remove(2)
            # NOTE: You may get a bug when two if statements have the same convergence point.
            # Becomes problamatic when you have no else statement in one or both of the if statements.
            # Will need to do some testing on this.

            return currCode, currNode, nodeDict

        # if guard block case (code 1) - this encompasses if-else and just plain if
        elif currNode.idCode is not None and 1 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # may want to check if you have an else block first
            elseFlag = 1  # 1 indicates that there IS an else block
            ifBlock = None  # ifBlock initially None
            elseBlock = None  # elseBlock initially None
            for tempNode in currNode.nextBlocks:
                # this is the convergence, there is no else
                if tempNode.idCode != None and 2 in tempNode.idCode:
                    elseFlag = 0  # 0 indicates no else

                # save the if block for later (this will catch if and else blocks if they both exist)
                else:
                    # IMPORTANT: We are assuming that the if node comes before the else block (fairly certain this will always be true)
                    if ifBlock == None:
                        ifBlock = tempNode
                    # if there are two blocks, this will catch the else block
                    else:
                        elseBlock = tempNode

            # add code for if block start
            currCode += "\nIF BLOCK START PLACEHOLDER {\n"

            # use the ifElseCodeHelper on the if statement
            newTuple = ifElseCodeHelper(ifBlock, nodeDict)
            newCode = newTuple[0]
            convergenceNode = newTuple[1]  # this may be None if it ended in Return
            nodeDict = newTuple[2]

            # add the code to the currCode
            currCode += newCode

            # add code for if block end
            currCode += "\nIF BLOCK END PLACEHOLDER }\n"

            # if there is an else block
            if elseFlag == 1:
                # add code for else block start
                currCode += "\nELSE BLOCK START PLACEHOLDER {\n"

                # use the ifElseCodeHelper on the else statement
                newTuple = ifElseCodeHelper(elseBlock, nodeDict)
                newCode = newTuple[0]

                # if the if block ended in a return, we will have a None here
                if convergenceNode == None:
                    convergenceNode = newTuple[1]  # technically this should be the same as above

                nodeDict = newTuple[2]

                # add the code to the currCode
                currCode += newCode

                # add code for else block end
                currCode += "\nELSE BLOCK END PLACEHOLDER }\n"

            # if there is no else block
            else:
                # add code for no else block ?
                currCode += "\nNO ELSE BLOCK PLACEHOLDER\n"
                # possibly need to link guard to not if somehow

            nodeDict[currNode] = True

            # it is possible that all paths ended in return
            if convergenceNode != None:
                queue.append(
                    convergenceNode)  # append the convergence node so that you will traverse it (we ignore the if branches we already searched)

            continue  # we don't add the currNode to the dict here since a convergence node can also be other things

        # while guard block case (code 3)
        elif currNode.idCode != None and 3 in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if 2 in currNode.idCode:
                currNode.idCode.remove(2)

            # add the code for start of while: while (statement) {
                # what exactly does this look like in SSA-LLVM ??
            currCode += "\nSTART OF WHILE (PLACEHOLDER STATEMENT) {\n"  # THIS IS OBVIOUSLY NOT CORRECT

            # NOTE: THIS IS ALSO WHERE WE CAN DEAL WITH THE m_bool, m_unary, m_binop IN THE GUARD STATEMENT
                # could also do it in _ssaGenerator if we want

            # traverse the while body using whileCodeHelper
            for tempNode in currNode.nextBlocks:
                # if you are looking at the body, traverse with whileCodeHelper
                if 4 in tempNode.idCode:

                    # THINKING I SHOULD PASS IN THE currNode and tempNode SO WE KNOW WHEN WE'VE REACHED THE ORIGINAL WHILE GUARD?
                    newTuple = whileCodeHelper(tempNode, currNode, nodeDict)
                    newCode = newTuple[0]
                    nodeDict = newTuple[1]

                    # add this new code to the currCode string
                    currCode += newCode

                # add the next (not body) node to the queue
                else:
                    queue.append(tempNode)

            # add the code for end of while: }
                # what exactly does this look like in SSA-LLVM ??
            currCode += "\nEND OF WHILE }\n"  # THIS IS OBVIOUSLY NOT CORRECT

            # add currNode to dict
            nodeDict[currNode] = True

            continue

        # body is typical (not an if or while component)
        else:
            for currLine in currNode.code:
                currCode += currLine

        # check if there are any next nodes, add them if so
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)

        # add the current node to the visited dict
        nodeDict[currNode] = True

    # this will be the code for each function (same order)
    return currCode, None, nodeDict

def generateFunctionTypes(prog:m_prog) -> dict:
    # create initial function dictionary
    funDict = {}

    # step through function and create the type tuple you need for the dict
    for fun in prog.functions:
        # create list of the functions parameter types
        paramTypeList = []
        for param in fun.param_declarations:
            paramTypeList.append(param.type)

        # add the current functions values into the function dictionary
        funDict[fun.id.identifier] = (fun.return_type, paramTypeList)

    return funDict

# given the head block of a function, step through and add previous blocks for each node
# returns current node connected to all of its previous nodes
def addPreviousBlocks(head:CFG_Node) -> CFG_Node:
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



# add empty block at the start and end of each while
# add empty block at the start and end of each if/if-else
# also add a return block for stack cleanup - all returns will point to this one cleanup point
# finally add an initial block that goes before the root of the program
# return node with empty blocks in correct spots
def addEmptyBlocks(head:CFG_Node) -> CFG_Node:
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