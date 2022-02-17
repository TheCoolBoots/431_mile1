from typing import Dict, Tuple
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import *
from generateLLVM import getLLVMType
from test_cfg_generator import *




# look at if and while loops
# step through the nodes of a function and put together a string of ssa code
# return this code
def addWhileIfCode(head):
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
def whileCodeHelper(head, guardNode, nodeDict):
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
    return (currCode, nodeDict)





# step thru the if/else nodes until you find a convergence block, another if guard, another while guard, or a dead end (return)
# each of these is a special case
# ONE MAIN DIFFERENCE FROM A WHILE STATEMENT IS THAT YOU MAY NEED TO RETURN THE CONVERGENCE BLOCK SO THAT YOU CAN CONTINUE WALKING THE NODES
def ifElseCodeHelper(head, nodeDict):
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

            return (currCode, currNode, nodeDict)



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
    return (currCode, None, nodeDict)











def tmp(prog:m_prog):
    # create a function node for each function
    functionList = generate_CFG_Prog_Handler(prog) # this is a list of function nodes



    # printCFG(functionList[len(functionList) - 1].firstNode)

    # generate globals, generate top_env, generate types
    # may need a new function for getting declarations in the global env
    lastReg = 0
    globalDeclarations = []
    for dec in prog.global_declarations:
        # get the list of code from the current declaration
        declarationList = dec.getSSA(lastReg, prog.getTypeSizes())  # return list of strings
        lastReg += 1  # increment by just 1?

        # extend the globalDeclarations list of code
        globalDeclarations.extend(declarationList)



    # getTopEnv(self, includeLineNum=True)
    # get the dictionary of string to type in the global environment
    globalTopEnv = prog.getTopEnv(False)


    # will need to step through each statement in each block in each function
    # convert to llvm code with - statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node)
    for fun in functionList:
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

            # add the current node to the visited dict
            nodeDict[currBlock] = True

            # will need to include global environment in the generateSSA function
            # _generateSSA(currentNode: CFG_Node, types, functions) : return code, currentNode.mappings
            tempCode, mappings = _generateSSA(currBlock, globalTopEnv, prog.getTypes(), generateFunctionTypes(prog)) # _generateSSA(currBlock, prog.getTypes(), generateFunctionTypes(prog), globalTopEnv)

            # update the ast code to be replaced with SSA LLVM code
            currBlock.code = tempCode
            currBlock.mappings = mappings # YES?

            # check if there are any next nodes, add them if so
            for tempNode in currBlock.nextBlocks:
                queue.append(tempNode)


            # anything else??


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
        currSSACode = addWhileIfCode(functionList[i].firstNode)
        # codeList.append(ssaCode)
        functionList[i].ssaCode = currSSACode
        i += 1


            # anything else??


    return functionList



def generateSSA(rootNode:CFG_Node, env, types, functions):
    # whiles and ifs
    
    pass


# top_env structure: {str: (bool, m_type)}              where bool == true if global, false if local 
# types structure: {str: list[m_declaration]}
# functions structure: {str: (m_type, list[m_type])}    maps funID -> return type, param types
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# functions structure: {str: (m_type, list[m_type])}     maps funID -> return type, param types
# {str funName: (m_type returnType, list[m_type] paramTypes)}
def generateFunctionTypes(prog:m_prog):
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

def _generateSSA(currentNode: CFG_Node, top_env:dict, types:dict, functions:dict):
    code = []
    lastRegUsed = currentNode.lastRegUsed
    statements = currentNode.code

    # print("ALL statements: " + str(statements))

    for statement in statements:
        lastRegUsed, llvmType, newCode = statementToSSA(lastRegUsed, statement, top_env, types, functions, currentNode)

        if newCode == -1:
            # print("currStatement: " + str(statement))

            # NEED TO WRITE CODE TO DEAL WITH UNARY, BINOP, AND BOOL HERE
            code.extend(["GUARD CODE PLACEHOLDER"])

            continue  # REMOVE continue ????

        code.extend(newCode)

    return code, currentNode.mappings


# env maps strings to types {str: bool, str(typeID)}
# r_ = load type[id] @z
# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
# returns a tuple containing (mappings within block, SSA LLVM code)
def statementToSSA(lastRegUsed:int, stmt, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match stmt:
        case m_assignment():
            return assignToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case m_print():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            if type(exprCode) == list:
                instruction = f'%{exprReg + 1} = call i32 @printf("%d", %{exprReg})'
                exprCode.append(instruction)
                return exprReg + 1, 'i32', exprCode
        case m_delete():
            exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, stmt.expression, env, types, functions, currentNode)
            if type(exprReg) != str:
                lastRegUsed = exprReg
            exprCode.extend([f'%{lastRegUsed + 1} = bitcast {exprType} %{exprReg} to i8*',
                            f'call void @free(%{lastRegUsed + 1})'])
            # env.pop(exprReg)
            return lastRegUsed + 1, 'void', exprCode
        case m_ret():
            return retToSSA(lastRegUsed, stmt, env, types, functions, currentNode)
        case other:
            print(f'ERROR: unrecognized structure:{other}')
            return -1, -1, -1


def retToSSA(lastRegUsed:int, ret:m_ret, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if ret.expression == None:
        return (lastRegUsed, 'void', [f'ret void'])

    returnReg, retType, returnCode = expressionToLLVM(lastRegUsed, ret.expression, env, types, functions, currentNode)
    if(retType == 'void'):
        returnCode.append(f'ret {retType}')
    else:
        returnCode.append(f'ret {retType} %{returnReg}')

    return (returnReg, retType, returnCode)


def assignToSSA(lastRegUsed:int, assign:m_assignment, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    exprReg, exprType, exprCode = expressionToLLVM(lastRegUsed, assign.source_expression, env, types, functions, currentNode)
    if type(exprReg) == int:
        lastRegUsed = exprReg
    targetStrings = [mid.identifier for mid in assign.target_ids]

    if len(targetStrings) == 1:
        # if the target is in the top_env, that means it is either a global var or global/local struct
        #       if global var, use @
        #       if local struct, use normal
        if targetStrings[0] in env:
            if env[targetStrings[0]] == m_type('int') or env[targetStrings[0]] == m_type('bool'):
                exprCode.append(f'store {exprType} %{exprReg}, i32* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # if struct is a global struct
            elif env[targetStrings[0]][0]:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} %{exprReg}, {typeStr}* @{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode
            # struct is a locally defined struct
            else:
                typeStr = getLLVMType(env[targetStrings[0]][1].typeID)
                exprCode.append(f'store {exprType} %{exprReg}, {typeStr}* %{targetStrings[0]}')
                return lastRegUsed, env[targetStrings[0]], exprCode

        # if it is not in top_env, it is a local variable and is dealt with through SSA form
        currentNode.mappings[targetStrings[0]] = (exprType, exprReg, 'placeholder')
        return exprReg, exprType, exprCode
    else:
        currentID = assign.target_ids[0].identifier
        currentIDTypeID = env[currentID][1].typeID
        
        nested = False
        for accessedm_id in assign.target_ids[1:]:
            nested = True
            accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

            if currentID in env and env[currentID][0]:
                instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
            else:
                instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
            exprCode.append(instruction)

            currentID = lastRegUsed + 1
            currentIDTypeID = accessedTypeID
            lastRegUsed += 1


        if currentIDTypeID == 'int' or currentIDTypeID == 'bool' or currentIDTypeID == 'null':
            exprCode.append(f'store i32 %{exprReg}, i32* %{currentID}')
            return lastRegUsed, 'i32', exprCode
        #(f'store %struct.s1* %1, %struct.s1** %2')
        else:
            if nested:
                llvmType = getLLVMType(currentIDTypeID)
                exprCode.append(f'store {llvmType} %{exprReg}, {llvmType}* %{currentID}')
                return lastRegUsed, llvmType, exprCode
            else:
                exprCode.append(f'%{currentID} = %{exprReg}')
                return lastRegUsed, getLLVMType(currentIDTypeID), exprCode
    

# returns a tuple containing (resultReg, llvmType, mappings within block, SSA LLVM code)
def expressionToLLVM(lastRegUsed:int, expr, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    match expr:
        case m_binop():
            return binaryToLLVM(lastRegUsed, expr, env, types, functions, currentNode)
        case m_num() | m_bool():
            return lastRegUsed+1, 'i32', [f'%{lastRegUsed+1} = i32 {expr.val}']
        case m_new_struct():
            # ASK PROFESSOR ABOUT THIS ON TUESDAY
            code = [f'%{lastRegUsed + 1} = call i8* @malloc({len(types[expr.struct_id.identifier]) * 4})',
                 f'%{lastRegUsed + 1} = bitcast i8* %{lastRegUsed + 1} to %struct.{expr.struct_id.identifier}*']
            return lastRegUsed+1, f'%struct.{expr.struct_id.identifier}*', code
        case m_null():
            # keeping it like this ensures functionality for rest of compiler
            return lastRegUsed+1, 'i32', [f'%{lastRegUsed+1} = i32 0']
        case m_invocation():
            return invocationToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_read():
            return lastRegUsed+2, 'i32', [f'%{lastRegUsed+2} = alloc i32', f'%{lastRegUsed+1} = call i32 @scanf("%d", %{lastRegUsed+2}*)']
        case m_unary():
            pass
        case m_dot():
            return dotToSSA(lastRegUsed, expr, env, types, functions, currentNode)
        case m_id():
            if expr.identifier in env:
                # if id is a global variable
                if env[expr.identifier][0]:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = load {llvmType}* @{expr.identifier}']
                else:
                    llvmType = getLLVMType(env[expr.identifier][1].typeID)
                    return lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = load {llvmType}* %{expr.identifier}']
            return readVariable(lastRegUsed, expr.identifier, currentNode)
        case other:
            print(f'ERROR: unrecognized expression: {other}')


def dotToSSA(lastRegUsed:int, expression:m_dot, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    currentID = expression.ids[0].identifier
    currentIDTypeID = env[currentID][1].typeID

    outputCode = []
    
    for accessedm_id in expression.ids[1:]:
        accessedIDmemNum, accessedTypeID = getNestedDeclaration(accessedm_id, types[currentIDTypeID])

        if currentID in env and env[currentID][0]:
            instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* @{currentID}, i32 0, i32 {accessedIDmemNum}'
        else:
            instruction = f'%{lastRegUsed + 1} = getelementptr %struct.{currentIDTypeID}, %struct.{currentIDTypeID}* %{currentID}, i32 0, i32 {accessedIDmemNum}'
        outputCode.append(instruction)

        currentID = lastRegUsed + 1
        currentIDTypeID = accessedTypeID
        lastRegUsed += 1

    currentIDTypeID = getLLVMType(currentIDTypeID)  # returns i32 or %struct.__*
    outputCode.append(f'%{lastRegUsed + 1} = load {currentIDTypeID}, {currentIDTypeID}* %{currentID}')

    return (lastRegUsed + 1, currentIDTypeID, outputCode)


# mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
def readVariable(lastRegUsed:int, identifier:str, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    if identifier in currentNode.mappings:
        return currentNode.mappings[identifier][1], currentNode.mappings[identifier][0], []
    else:
        if not currentNode.sealed:
            currentNode.mappings[identifier] = ('?', lastRegUsed+1)
            return lastRegUsed+1, '?', [f'%{lastRegUsed + 1} = phi(_)']
        elif len(currentNode.previousBlocks) == 0:
            # val is undefined
            # should never encounter this case
            pass
        elif len(currentNode.previousBlocks) == 1:
            # call expressionToLLVM with expr and prev block's mappings
            prevNode = currentNode.previousBlocks[0]
            return readVariable(lastRegUsed, identifier, prevNode)
        else:
            # create phi node with values in prev blocks
            possibleRegisters = [readVariable(lastRegUsed, identifier, node) for node in currentNode.previousBlocks]
            llvmType = possibleRegisters[0][1]
            phiParams = [f'{reg[1]} %{reg[0]}' for reg in possibleRegisters]
            phiParams = ', '.join(phiParams)

            # map variable to phi node
            currentNode.mappings[identifier] = (llvmType, lastRegUsed+1)
            return (lastRegUsed+1, llvmType, [f'%{lastRegUsed+1} = phi({phiParams})'])


# == != <= < > >= - + * / || &&
def binaryToLLVM(lastRegUsed:int, binop:m_binop, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    leftOpReg, leftLLVMType, leftOpCode = expressionToLLVM(lastRegUsed, binop.left_expression, env, types, functions, currentNode)
    rightOpReg, rightLLVMType, rightOpCode = expressionToLLVM(leftOpReg, binop.right_expression, env, types, functions, currentNode)

    # == != <= < > >= - + * / || &&
    match binop.operator:
        case '==':
            op = 'icmp eq i32'
        case '!=':
            op = 'icmp ne i32'
        case '<=':
            op = 'icmp sle i32'
        case '<':
            op = 'icmp slt i32'
        case '>=':
            op = 'icmp sge i32'
        case '>':
            op = 'icmp sgt i32'
        case '-':
            op = 'sub i32'
        case '+':
            op = 'add i32'
        case '*':
            op = 'mul i32'
        case '/':
            op = 'div i32'
        case '||':
            op = 'or i32'
        case '&&':
            op = 'and i32'

    instructions = []
    targetReg = rightOpReg + 1
    instructions.extend(leftOpCode)
    instructions.extend(rightOpCode)
    instructions.append(f'%{targetReg} = {op} %{leftOpReg}, i32 %{rightOpReg}')

    return (targetReg, 'i32', instructions)


def invocationToSSA(lastRegUsed:int, exp:m_invocation, env:dict, types:dict, functions:dict, currentNode:CFG_Node) -> Tuple[int, str, list[str]]:
    params = []
    for expression in exp.args_expressions:
        params.append(expressionToLLVM(lastRegUsed, expression, env, types, functions, currentNode))
        lastRegUsed = params[-1][0]

    targetReg = params[-1][0] + 1
    returnTypeID = getLLVMType(functions[exp.id.identifier][0].typeID)
    funID = exp.id.identifier

    parameters = []
    instructions = []

    for paramReg, paramType, paramCode in params:
        parameters.append(f'{paramType} %{paramReg}')
        instructions.extend(paramCode)
    
    # join them into TYPE REG, TYPE REG, TYPE REG format
    parameters = ', '.join(parameters)
            
    instructions.append(f'%{targetReg} = call {returnTypeID} @{funID}({parameters})')

    return (targetReg, returnTypeID, instructions)


# returns (struct member num, member typeID)
def getNestedDeclaration(id:m_id, declarations: list[m_declaration]) -> Tuple[int, str]:
    for i, decl in enumerate(declarations):
        if decl.id == id:
            return (i, decl.type.typeID)


# Placeholder for phi node
# ASK PROFESSOR ABOUT THIS ON THURSDAY
class phi:
    def __init__(self, lst:list, complete = False):
        self.possibleValues = lst
    def getPlaceHolder():
        return 'i32', 0