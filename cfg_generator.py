import ...

class CFG_Node:
    def __init__(self, previousBlocks:list[CFG_Node], nextBlocks:list[CFG_Node], code:list, returnType: ___ = None): 
        self.previousBlocks = previousBlocks # can be multiple
        self.nextBlocks = nextBlocks # could be multiple
        self.code = code
        self.returnType = returnType # default is currently None, might wanna do m_type("void") instead, also should probably add a type


# GLOBAL FUNCTION BLOCK ENVIRONMENT
functionBlocks = {} 


def generate_CFG_Prog_Handler(program:m_prog):

    # look through the functions and make them into blocks (in order)
    for fun in program.functions:
        # if you get to main, break, this is a special case (??)
        if(fun.id.identifier) == "main":
            break
        # create block for each function
        newNode = generate_CFG_Function_Handler(fun.statements)

        # add the new block to the environment
        functionBlocks[fun.id] = newNode


    # once we get to main we will continue making blocks but also piecing together the other functions
    # WHAT DO WE DO WITH MAIN HERE

    




# handle each function uniquely, step through statements and create/connect nodes as needed
def generate_CFG_Function_Handler(currStatements:list): # WAS def generate_CFG_Function_Handler(currFunction:m_function):

    # create a node
    currNode = CFG_Node([], [], [])

    initialNode = currNode
    

    # run this node through the statements until we need a new one
    for statement in currStatments:


        # CONSIDER JUST PUTTING THE generate_CFG_Nodes() FUNCTION CODE HERE INSTEAD OF CALLING IT
            # THIS WOULD FIX THE ISSUE WHERE WE CANT PASS BY ADDRESS, ONLY REFERENCE
            # I may not need to do this but I am unsure at the moment

        
        # add to curr node based on current statement
        # NOTE: if we look at an if else/while statement, we return the guard node so that we can connect the nodes
        currTuple = generate_CFG_Nodes(statement, currNode)

        # i need to do this since python doesnt pass by reference
        currNode = currTuple[0]


        # might be a weird edge case on the last statement
        # check if we need a new node (if or while)
        if(currTuple[1] > 1):
            newNode = CFG_Node([], [], [])
            
            
            # while statement, connect the returned guard node to the new node
            if(currTuple[1] == 2):
                # simply put the newNode as a nextBlock from currNode and ...
                currNode.nextBlocks += newNode

                # put the currNode as a previous block from the newNode
                newNode.previousBlocks += currNode

                # update currNode to be newNode
                currNode = newNode


            # if else statment, connect each existing next from the guard block to the new node
            else:
                # get the if node and also the else node if it exists
                ifNode = currBlock.nextBlocks[0]

                # simply put the newNode as a nextBlock from both the if and else Nodes and ...
                ifNode.nextBlocks += newNode 

                # put the if node and else nodes as previous blocks from the newNode
                newNode.previousBlocks += ifNode 

                # do all the same for the else node if it exists
                if len(currBlock.nextBlocks) > 1:
                    elseNode = currBlock.nextBlocks[1]
                    elseNode.nextBlocks += newNode 
                    newNode.previousBlocks += elseNode 

                # update currNode to be newNode
                currNode = newNode


        # reached function invocation error in block
        elif(currTuple[1] == -1):
            # there are no valid nodes to return (make sure this is what you want)
            return None
            

        # reached return in main block
        elif(currTuple[1] == 1)
            # break from the function, no need to go further (shouldnt really be any more in reality)
            break
    
    # youve reached the end of the function, return the intial node
    return initialNode

        






# add the code to the current node, if and while will do weird things
# DO I WANT TO CALL THIS WITH MULTIPLE EXPRESSIONS???? OR JUST 1 AT A TIME??

# returns a tuple that is (node, int) - 
    # return 0 if you can just continue
    # 1 if it is a return statment
    # 2 if it is an invocation
    # 3 if it is a while statment 
    # 4 if it is an if/if else statement
# add to the current node, when you get 
def generate_CFG_Nodes(expression, currNode):
    match expression:

        # conditional → if ( expression ) block {else block}opt
        # GUARD STATMENT IS ITS OWN BLOCK
        case m_conditional():
            # call generete_CFG_Nodes on the guard statment, set this to next from the current node
            currTuple = generate_CFG_Function_Handler([expression.guard_expression]) # DOUBLE CHECK SYNTAX

            # if you got a function environment error
            if(currTuple[0] == None or currTuple[1] == -1):
                # make sure this is what you want
                return None

            guardNode = currTuple[0]

            currNode.nextBlocks += guardNode


            # call generete_CFG_Nodes on the new branch, set this to next from the guard node
            ifNode = generate_CFG_Function_Handler(expression.if_statements)
            if(ifNode == None):
                return None
            guardNode.nextBlocks += ifNode
            ifNode.previousBlocks += guardNode


            # check if there is an else
            if expression.else_statments != [None]:

                # call generate_CFG_Nodes on this new branch with its statments and also set this to next from the guard node
                elseNode = generate_CFG_Function_Handler(expression.else_statements)
                if(elseNode == None):
                    return None
                guardNode.nextBlocks += elseNode
                elseNode.previousBlocks += guardNode



            # somehow we need to set the next of both if and else to the next statement
                # shouldnt this be done in the upper level function?


            # what should we return?

            return (guardNode, 3) # make sure this is actually what you want


        # loop → while ( expression ) block
        # GUARD STATMENT IS ITS OWN BLOCK
        case m_loop():
            # call generete_CFG_Nodes on the guard statment, set this to next from the current node
            currTuple = generate_CFG_Function_Handler([expression.guard_expression])
            guardNode = currTuple[0]
            if guardNode == None or currTuple[1] == -1:
                return None
            
            # its next should be the while statements and also the code after it



            # call generete_CFG_Nodes on the statement in the while
            currTuple = generate_CFG_Function_Handler(expression.body_statements)
            whileNode = currTuple[0]
            if whileNode == None or currTuple[1] == -1:
                return None
            
            # set this to next from the guard node, next from this should also be the guard node
            guardNode.nextNodes += whileNode
            whileNode.nextNodes += guardNode

            # return the guard node
            return (guardNode, 2)


        # ret → return {expression}opt;
        case m_ret():

            # set the return type of the current node
            currNode.returnType = ... # MIGHT NEED SOME SORT OF FUNCTION TO GET THE TYPE FROM me_ret.expression



            return (currNode, 1)



# THIS FUNCTION ISNT DONE YET
        # THINK MORE ABOUT HOW YOU WILL RETURN FROM THIS CASE
        # invocation → id arguments ;
        case m_invocation():
            # function not in environment case
            if(expression.id.identifier not in functionBlocks):
                return (currNode, -1)


            # patch the node from the dictionary on the current head

            

            # I DONT THINK I NEED TO DO ANYTHING SPECIAL AFTER RETURN 
            return (____, 0) # WAS 2 HERE NOW IS 0


        # there shouldnt be anymore special case structs 
        case _:
            # add the code to the current list, continue to the next bit
            currNode.code += expression
            return (currNode, 0)



