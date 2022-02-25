from typing import Dict, Tuple
from ast_class_definitions import *
from cfg_generator import *
from ssaGenerator import generateSSA
from ssaGenerator import expressionToSSA
import copy




def branchesToSSA(lastRegUsed: int, head: CFG_Node, guardNode: CFG_Node, nodeDict: dict, ifFlag: int, whileFlag: int) -> Tuple[list[str], CFG_Node, dict]:
    # nodeDict = {}               # make dict of traversed nodes
    queue = []  # make queue for traversing nodes
    queue.append(head)  # start off the queue
    currCode = []  # this is the code from the current function

    # step through each block of current tree and find the if and while statements
    while queue != []:
        currNode = queue.pop(0)  # take first item from the queue

        # check if youve already looked at this node
        if currNode in nodeDict:
            continue

        # # add the current node to the visited dict
        # nodeDict[currNode] = True

        # if convergence block case (code 2)
        if ifFlag == 1 and currNode.idCode is not None and IdCodes.IF_CONVERGENCE in currNode.idCode:

            # SPECIAL CASE!
            # YOU FOUND THE CONVERGENCE BLOCK, THIS MEANS THAT YOU CAN RETURN THE CODE YOU HAVE SO FAR
            # YOU SHOULD PROBABLY RETURN THIS NODE (along with the accumulated code) SO THAT YOU CAN CONTINUE WALKING THE NODES
            # IMPORTANT NOTE! DONT ADD THE CODE FROM THIS TO YOUR CODE FIELD.
            # YOU WILL WANT TO DO THAT IN THE HIGHER LEVEL FUNCTION.

            # We remove the code so that if this is a doubly nested call, the convergence node doesnt confuse us.
            currNode.idCode.remove(IdCodes.IF_CONVERGENCE)
            # NOTE: You may get a bug when two if statements have the same convergence point.
            # Becomes problamatic when you have no else statement in one or both of the if statements.
            # Will need to do some testing on this.

            return currCode, currNode, nodeDict



        # if guard block case (code 1) - this encompasses if-else and just plain if
        elif currNode.idCode is not None and IdCodes.IF_GUARD in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if IdCodes.IF_CONVERGENCE in currNode.idCode:
                currNode.idCode.remove(IdCodes.IF_CONVERGENCE)

            # may want to check if you have an else block first
            elseFlag = 1  # 1 indicates that there IS an else block
            ifBlock = None  # ifBlock initially None
            elseBlock = None  # elseBlock initially None
            for tempNode in currNode.nextBlocks:
                # this is the convergence, there is no else
                if tempNode.idCode != None and IdCodes.IF_CONVERGENCE in tempNode.idCode:
                    elseFlag = 0  # 0 indicates no else

                # save the if block for later (this will catch if and else blocks if they both exist)
                else:
                    # IMPORTANT: We are assuming that the if node comes before the else block (fairly certain this will always be true)
                    if ifBlock == None:
                        ifBlock = tempNode
                    # if there are two blocks, this will catch the else block
                    else:
                        elseBlock = tempNode

            # IF STATEMENT HANDLING
            currCode.append(f'br i32 %{currNode.lastRegUsed}, label %{lastRegUsed + 1}, label %{lastRegUsed + 2}')
            currCode.extend(currNode.code)
            currCode.append(f'{lastRegUsed + 1}:')

            newCode, convergenceNode, nodeDict = branchesToSSA(lastRegUsed + 2 + int(elseFlag), ifBlock, None, nodeDict,
                                                               1, 0)

            currCode.extend(newCode)
            if elseFlag == 1:
                currCode.append(f'br label %{lastRegUsed + 3}')
            currCode.append(f'{lastRegUsed + 2}:')

            if elseFlag == 1:
                # add code for else block start
                # use the ifElseCodeHelper on the else statement
                newCode, tmp, nodeDict = branchesToSSA(lastRegUsed + 3, elseBlock, None, nodeDict, 1, 0)

                # if the if block ended in a return, we will have a None here
                if convergenceNode == None:
                    convergenceNode = tmp  # technically this should be the same as above

                # add the code to the currCode
                currCode.extend(newCode)

                # add code for else block end
                currCode.append(f'{lastRegUsed + 3}:')

            nodeDict[currNode] = True

            if elseFlag == 1:
                lastRegUsed += 3
            else:
                lastRegUsed += 2

            # it is possible that all paths ended in return
            if convergenceNode != None:
                queue.append(
                    convergenceNode)  # append the convergence node so that you will traverse it (we ignore the if branches we already searched)

            continue  # we don't add the currNode to the dict here since a convergence node can also be other things



        # THIS NEEDS TO INCORPERATE THE NEW whileFlag IN THIS STATMENT
        # while guard block case (code 3) - the one that you passed in
        elif whileFlag == 1 and currNode.idCode != None and IdCodes.WHILE_GUARD in currNode.idCode and currNode.id == guardNode.id:

            # anything we need to do here????

            # THIS IS AN IMPORTANT SPECIAL CASE WHERE YOU FIND THE ORIGINAL GUARD BLOCK.
            # YOU WILL RETURN BACK WITH ALL THE CODE YOU'VE ACCUMULATED SO THAT THE UPPER LEVEL FUNCTION CAN DEAL WITH IT.

            return currCode, None, nodeDict



        # while guard block case (code 3)
        elif currNode.idCode != None and IdCodes.WHILE_GUARD in currNode.idCode:

            # potential bug here where the guard appears to be a convergence
            if IdCodes.IF_CONVERGENCE in currNode.idCode:
                currNode.idCode.remove(IdCodes.IF_CONVERGENCE)

            # WHILE STATEMENT HANDLING
            currCode.extend(currNode.code)
            currCode.extend([f'{lastRegUsed + 1}:',
                             f'br i32 %{currNode.lastRegUsed}, label %{lastRegUsed + 2}, label %{lastRegUsed + 3}',
                             f'{lastRegUsed + 2}:'])

            # traverse the while body using whileCodeHelper
            for tempNode in currNode.nextBlocks:
                # if you are looking at the body, traverse with whileCodeHelper
                if IdCodes.WHILE_BODY in tempNode.idCode:

                    # THINKING I SHOULD PASS IN THE currNode and tempNode SO WE KNOW WHEN WE'VE REACHED THE ORIGINAL WHILE GUARD?
                    newCode, nodeDict = branchesToSSA(lastRegUsed + 3, tempNode, currNode, nodeDict, 0, 1)
                    currCode.extend(newCode)

                # add the next (not body) node to the queue
                else:
                    queue.append(tempNode)

            currCode.append(f'br %{lastRegUsed + 1}')
            currCode.append(f'{lastRegUsed + 3}:')

            lastRegUsed += 3

            nodeDict[currNode] = True
            continue

        # body is typical (not an if or while component - could technically be a while body or if convergence)
        else:
            # # shouldnt get an if convergence or while body here
            # if currNode.idCode != None and (IdCodes.IF_CONVERGENCE in currNode.idCode or IdCodes.WHILE_BODY in currNode.idCode):
            #     print("\nWHY IS THIS HAPPENING\n\n")

            for currLine in currNode.code:
                currCode.append(currLine)

        # check if there are any next nodes, add them if so
        for tempNode in currNode.nextBlocks:
            queue.append(tempNode)  # might want to pre-screen nodes before adding them to save some extra time

        # add currNode to the dictionary
        nodeDict[currNode] = True

    # this is the return for an if branch
    if whileFlag == 1:
        # this return signifies that we finished the queue without finding the original while guard (reached a return statement)
        return currCode, None, nodeDict

    # this is the return for a while branch
    elif ifFlag == 1:
        # this will be the code for each function (same order)
        return currCode, None, nodeDict

    # this is the return of the whole functions code
    else:
        return currCode, None , None
