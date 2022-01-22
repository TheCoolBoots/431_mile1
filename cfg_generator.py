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

        # create block for each function
        newNode = generate_CFG_Function_Handler(fun)

        # add the new block to the environment
        functionBlocks[fun.id] = newNode


    #  once we get to main we will continue making blocks but also piecing together the other functions



# handle each function uniquely, step through statements and create/connect nodes as needed
def generate_CFG_Function_Handler(currFunction:m_function):

    # create a node
    currNode = CFG_Node([], [], [])

    initialNode = currNode
    

    # run this node through the statements until we need a new one
    for statement in currFunction.statements:


        # add to curr node based on current statement
        # NOTE: if we look at an if else/while statement, we return the guard node so that we can connect the nodes
        currTuple = generate_CFG_Nodes(statement, currNode)

        # i think i need to do this since python doesnt pass by reference
        currNode = currTuple[0]


        # might be a weird edge case on the last statement
        # check if we need a new node
        if(currTuple[1] > 2):
            newNode = CFG_Node([], [], [])
            
            
            # while statement, connect the returned guard node to the new node
            if(currTuple[1] == 3):
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
                    elseNode.previousBlocks += elseNode 

                # update currNode to be newNode
                currNode = newNode



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



            # call generete_CFG_Nodes on the new branch, set this to next from the guard node



            # check if there is an else
                # call generate_CFG_Nodes on this new branch with its statments and also set this to next from the guard node



            # somehow we need to set the next of both if and else to the next statement



            # what should we return?

            return (___, 4)


        # loop → while ( expression ) block
        # GUARD STATMENT IS ITS OWN BLOCK
        case m_loop():
            # call generete_CFG_Nodes on the guard statment, set this to next from the current node
                # its next should be the while statements and also the code after it




            # call generete_CFG_Nodes on the statement in the while
                # set this to next from the guard node, next from this should also be the guard node



            # what should we return?


            return (____, 3)


        # ret → return {expression}opt;
        case m_ret():





            return (____, 1)




        # THINK MORE ABOUT HOW YOU WILL RETURN FROM THIS CASE
        # invocation → id arguments ;
        case m_invocation():
            # patch the node from the dictionary on the current head





            return (____, 2)


        # there shouldnt be anymore special case structs 
        case _:
            # add the code to the current list, continue to the next bit
            currNode.code += expression
            return (currNode, 0)



