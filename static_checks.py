from ast_class_definitions import *

"""
TASK 3: static semantic checks
    TASK 3a: type checking
        recursively determine if m_program object conforms to typing restrictions
        NOTE this seems to be just about the same as type checking assignment from 430
            uses Type Environment to store ids and recursively parses through the program
    TASK 3b: function returns
        ensure every path through a function results in a valid return and return type
        NOTE not sure how to do this one yet; probably just some recursive calls on the functions
            list as defined in overview.pdf. 
"""

# CONSIDER ADDING A GLOBAL TO SEE WHERE THE TYPE CHECKER FOUND THE ISSUE



# return False if it is invalid and True if it is valid
def type_check(expression ,localTypeEnvironment: dict):
    # step through each expression 
    expressionType = type(expression)


# "Structure names are in a separate namespace from variables and functions."
    # does this imply that we should have varaibles and functions share an environment??
    # or should I have a seperate environment for functions???


    # declare my two global environments - make sure a global struct environment seperate from variables makes sense
    globalTypeEnvironment = {}
    globalStructEnvironment = {}
    # dictionary of string ids each mapped to a dictionary of mappings from string to string types
    # {A : {a : int, b : int}} 


    # m_prog 
    # this branch returns True OR False instead of the environment or False
    if expressionType is m_prog:
        print("MATCHED")

        # step through the global declarations and add them to the global type environment
        for i in expression.global_declarations:
            # create and extend the global environment 
            # HERE I AM ASSUMING THAT i.type is a valid type
            globalTypeEnvironment = extendEnv(globalTypeEnvironment, i.id, i.type) # does extendEnv check for duplicate variables in the env? 
            
            # if you get an illegal type, return False
            if globalTypeEnvironment == False:
                return False


        # step through the global structs and add them to the global struct environment
        for j in expression.type_declarations:
            # I think I need to make the global struct environment here
            # decided that extendEnv will be able to do the needed work
            # HERE I AM ASSUMING THAT i.nested_declarations is a valid type
            globalStructEnvironment = extendEnv(globalStructEnvironment, j.id, j.nested_declarations) # does extendEnv check for duplicate variables in the env? 
            
            # if your global struct environment has a type error, return False
            if globalStructEnvironment == False:
                return False


        for k in expression.functions:
            # functions should go into the global type env
            # I will make that happen in the m_function branch of type_check

            # run each function through the type checker to be sure that it is valid
            if(type_check(k, localTypeEnvironment) == False):
                return False
            

        # if you havent returned False at this point, the typing of the program should be valid
        return True


    # m_type
    elif expressionType is m_type:
        print("MATCHED")
        # check if you have type string OR a valid id in the local/global env OR a valid id for a strutc
        if expression.type == "int" or expression.type == "bool" or expression.type == "void" or expression.type in localTypeEnvironment or expression.type in globalTypeEnvironment or expression.type in globalStructEnvironment:
            # success, return the local environment
            return typeEnviroment
        else:
            # failure, return False 
            return False


    # m_declaration 
    elif expressionType is m_declaration:
        print("MATCHED")
        # add the binding to the environment
        # can have:
            # int a;  => this is a declaration
        # but not:
            # a = 1;  => this is an statement and the sub group is assignment

        # the extendEnv function should do the check for us to see if an id already exists in the environment
        # extend the environment to have the id-type mapping
        # HERE I AM ASSUMING THAT expression.type is a valid type
        return extendEnv(localTypeEnvironment, expression.id, expression.type) 

            
    # m_bool
    elif expressionType is m_bool:
        print("MATCHED")
        # nothing to do here? just return back environment
        return localTypeEnvironment


    # m_null
    elif expressionType is m_null:
        print("MATCHED")
        # nothing to do here? just return back environment
        return localTypeEnvironment


    # m_num
    elif expressionType is m_num:
        print("MATCHED")
        # nothing to do here? just return back environment
        return localTypeEnvironment


    # m_num
    elif expressionType is m_num:
        print("MATCHED")
        # nothing to do here? just return back environment
        return localTypeEnvironment


    # m_function 
    elif expressionType is m_function:
        print("MATCHED")

        # check that there isnt already a function with this name???? would need to have a function env???
        # save the environment before you mess with it so you can return it as it was (scoping)
        initialEnv = localTypeEnvironment

        # run type_check on the params to get the parameter types into the environment for the function
        for i in expression.param_declarations:
            localTypeEnvironment = type_check(i, localTypeEnvironment)
            if localTypeEnvironment == False:
                return False

        # need to also get the body declarations into the environment
        for j in expression.body_declarations:
            # DO WE WANT TO CHECK THE LINE NUMBERS HERE??? OR ON A LOWER LEVEL???
            localTypeEnvironment = type_check(j, localTypeEnvironment)
            if localTypeEnvironment == False:
                return False

        # count how many statements are in the statements
        numStatments = 0
        for k1 in expression.statements:
            numStatments += 1

        currCount = 0
        # run type-check on each statement in the statement list
        for k2 in expression.statements:
            # get the return type for each function recursively
            actualReturnType = getType(k2, localTypeEnvironment) 

            # check if you are returning before the end of the block
            if type(k2) == m_ret and currCount != (numStatments + 1):
                return False

            currCount += 1

        # check that the return type matched the return statement type of the function
        if actualReturnType != expression.return_type:
            return False

        # put the function into the global type environment, here is what im thinking:
        # {id : [lineNum, param_declarations, return_type, body_declarations, statements], id2 : [ ... ], ...}
        globalTypeEnvironment = extendEnv(globalTypeEnvironment , expression.id , [expression.lineNum, expression.param_declarations, expression.return_type, expression.body_declarations, expression.statements])
        if globalTypeEnvironment == False:
            return False

        # return the initial environment unchanged
        return initialEnv


    # m_assignment 
    elif expressionType is m_assignment:
        print("MATCHED")

        # this function will get the return type back form a source_expression - similar to the one i need for return type
        currType = getType(expression.source_expression, localTypeEnvironment)

        # check that the output type of source_expression matches each id location in the environment
        for i in expression.target_ids:
            if localTypeEnvironment[i] != currType:
                return False

        # return the environment (shouldnt be changed)
        return localTypeEnvironment


    # m_ret 
    elif expressionType is m_ret:
        print("MATCHED")
        # dont think I really need to do anything except ensure that the return statement is type valid
        if type_check(expression.expression, localTypeEnvironment) == False:
            return False

        # return unchanged environment
        return localTypeEnvironment


    # m_print 
    # biggest question: can we print a struct?? - no:
    # "print requires an integer argument and outputs the integer to standard out"
    elif expressionType is m_print:
        print("MATCHED")
        if getType(expression.expression) != m_int:
            return False
        return localTypeEnvironment







# FROM HERE DOWN I WANT VALIDATION WITH EACH CASE




    # verify that i understand this correctly
    # m_conditional
    elif expressionType is m_conditional:
        print("MATCHED")

        # get the return type of expression
        expressionType = getType(expression.guard_expression, localTypeEnvironment)
        
        # if it isnt bool, return False
        if expressionType != m_bool: 
            return False

        ifReturnType = m_type("void")
        # call type check on each statement - just making sure that they are type sound
        for i in expression.if_statements:
            if type_check(i, localTypeEnvironment) == False:
                return False
            if type(i) == m_ret

        # if there is an else block, type check each statement
        if expression.else_statements != None:
            for j in expression.else_statements:
                if type_check(j, localTypeEnvironment) == False:
                    return False

        return localTypeEnvironment
 


    # m_loop 
    elif expressionType is m_loop:
        print("MATCHED")

        # get the return type of expression
        expressionType = getType(expression.guard_expression, localTypeEnvironment)

        # if it isnt bool, return False
        if expressionType != m_bool: # MAKE SURE THIS IS THE RIGHT WAY TO CHECK!!!!
            return False

        for i in body_statements:
            if type_check(i, localTypeEnvironment) == False:
                return False

        # i think this is right, dont see why I would extend the environment
        return localTypeEnvironment


# UNFINISHED, NOT IMPLEMENTED QUITE YET
    # THIS IS DEFINITELY WRONG IF SELECTOR ISNT IN THE LANGUAGE
    # maybe i dont have to worry about the operator and only selector?
    # m_unary 
    elif expressionType is m_unary:
        print("MATCHED")

        # IS THIS ALL I NEED???
        if type_check(expression.selector, localTypeEnvironment) == False:
            return False

        return localTypeEnvironment 










# FROM HERE DOWN I NEED HELP WITH AT LEAST PART OF EACH CASE


    # I DONT UNDERSTAND WHAT THIS DOES, MAYBE DELISTING AN ID FROM THE ENVIRONMENT???
    # m_delete 
    elif expressionType is m_delete:
        print("MATCHED")
    # my thought is that expression MUST evaluate to an id, and that id should be removed from the environment
        
        # type check the expression
        type_check(expression.expression) 

        # somehow get the id from the expression
        .....

        # first gotta check which environment its in
        ...

        # then delete it
        del localTypeEnvironment['Mani']

        # probably do local -> global -> structs




    # DONT UNDERSTAND WHAT THIS DOES YET
    # m_invocation 
    elif expressionType is m_invocation:
        print("MATCHED")
    # this is function calls
    # arg_expressions is the arguments to the function



    # CLOSE BUT STILL HAVE A LINGERING QUESTION ON STRUCTS
    # maybe i dont have to worry about the operator and only expression types?
    # m_binop
    elif expressionType is m_binop:
        print("MATCHED")

        # get the type of each expression
        leftType = getType(expression.left_expression, localTypeEnvironment)
        rightType = getType(expression.right_expression, localTypeEnvironment)

        # decided to implement it as possible to compare structs, just check that the structs have the same type
        # these operators are more flexible, allow for (int, int) or (bool, bool)
        if expression.operator == '!=' or '==':
        
            # case with 2 ints
            if leftType == m_int and rightType == m_int:
                pass

            # case with 2 bools
            elif leftType == m_bool and rightType == m_bool:
                pass
            
            # case with 2 structs (must be the same struct id)
            elif leftType == m_id and rightType == m_id and leftType.identifier == rightType.identifier:
                pass

            else:
                return False

        # these operators are less flexible, only allow for (int, int) 
        elif expression.operator == '<' or '>' or '<=' or '>=' or '+' or '-' or '/' or '*':
            # same function as before, expecting to get the type of an expression
            if leftType != m_int or rightType != m_int:
                return False

        return localTypeEnvironment




    # m_declarations 
    elif expressionType is m_declarations:
        print("MATCHED")
        # YOU SHOULD UPDATE THE ENVIRONMENT AS YOU STEP THROUGH THE declarations
        # EACH ONE NEEDS TO HAVE THE UPDATES FROM THE PREVIOUS ONE
        for i in expression.declarations:
            # add the type for each expression to the type environment
            localTypeEnvironment = type_check(i, localTypeEnvironment)
            
            # if the type_check returned false on a lower level, return False
            if localTypeEnvironment == False:
                return False
        return localTypeEnvironment



# {id : {id : type, id : type}}
    # THESE INDICATE ALL OF THE STRUCTS
    # I AM UNSURE WHAT TO DO HERE
    # m_type_declaration → struct id { nested decl } ;
    elif expressionType is m_type_declaration:
        print("MATCHED")

        # step through the structs declarations and put them in some environment (maybe use a temp local?)
        for i in expression.nested_declarations:
            # need to update the struct environment as you walk through
            # DO I NEED TO MAKE A NEW FUNCTION TO TRAVERSE AND EXTEND STRUCTS INTO THE ENVIRONMENT???
            globalStructEnvironment = extendEnv(globalTypeEnvironment, __id__, __type__)
            if globalStructEnvironment == False:
                return False

            # localTypeEnvironment = type_check(i, localTypeEnvironment)
            # if localTypeEnvironment == False:
            #     return False

        # return the unchanged initial environment
        return localTypeEnvironment
        




# another big question:
    # when looking through the 3 (?) environments to type check, would we look at local->struct->global OR local->global->struct
    # still unsure
    else:
        print("FAILED TO RECOGNIZE TYPE")
        return False









# ARE ALL OF THESE JUST NOT IN USE ANY MORE????
    # # FOR NOW, THIS WILL BE OUT
    #     # m_selector 
    #     elif expressionType is m_selector:
    #         print("MATCHED")

    # # WHAT IS THIS???
    #     # m_factor  _(expression)_
    #     elif expressionType is m_factor:
    #         print("MATCHED")

    # # m_statement 
    # elif expressionType is m_statement:
    #     print("MATCHED") 

    # # I AM THINKING THAT I COULD HAVE statement_list GIVE THE ACTUAL RETURN TYPE
    # # m_statement_list 
    # elif expressionType is m_statement_list:
    #     print("MATCHED")

    # # REPLACED AS WELL ???
    # # m_block 
    # elif expressionType is m_block:
    #     print("MATCHED")

    # # NOT IN USE???
    # # when you have a struct and want to access values in it 
    # # so like when you do A.b
    # # m_lvalue 
    # elif expressionType is m_lvalue:
    #     print("MATCHED")

    # # list of all the structs in a program
    # # m_types → {type declaration}∗
    # elif expressionType is m_types:
    #     print("MATCHED")
    #     # dont need to type check structs, that will happen (if you want) in the m_types class
    #     return localTypeEnvironment

    # # ADD SOMETHING TO THE ENVIRONMENT
    # # m_functions 
    # elif expressionType is m_functions:
    #     print("MATCHED")

    #     for i in expression.functions:
    #         type_check(i, localTypeEnvironment)  
    
    #     return localTypeEnvironment


    # MAKE SURE THIS IS PROPER SYNTAX
    # my thought here is that if we are given None (return type I assume) we just say that 
    # its fine and return the environment.
    # elif expressionType is None: 
    #     return localTypeEnvironment
    # wont actually hit this, we would instead get to m_null
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^




# these were previously ruled out

    # # m_decl 
    # elif expressionType is m_decl:
    #     print("MATCHED")

    # # m_expression
    # elif expressionType is m_expression:
    #     print("MATCHED")

    # # m_eqterm 
    # elif expressionType is m_eqterm:
    #     print("MATCHED")


    # # m_relterm 
    # elif expressionType is m_relterm:
    #     print("MATCHED")

    # # m_simple 
    # elif expressionType is m_simple:
    #     print("MATCHED")

    # # m_term 
    # elif expressionType is m_term:
    #     print("MATCHED")

    # # m_parameters 
    # elif expressionType is m_parameters:
    #     print("MATCHED")

    # # m_nested_decl → decl ; {decl ;}∗
    # elif expressionType is m_nested_decl:
    #     print("MATCHED")


    # # m_id_list → id {,id}∗
    # elif expressionType is m_id_list:
    #     print("MATCHED")
    #     for i in expression.id_list:
    #         if i == "int" or i == "bool" or i in typeEnvironment:
    #             continue
    #         else:
    #             return False

    # # m_return_type
    # elif expressionType is m_return_type:
    #     print("MATCHED")





# I MAY NEED TO CHECK IF A VARIABLE IS IN THE GLOBAL ENVIRONMENT SOMEWHERE - I think local and global environments can contain collisions between??
# will probably want to return false if you try to extend with a duplicate variable name
# if someone does: int i; when there is an int i; in the global scope, I dont think that would be legal.
def extendEnv(typeEnvironment: dict, currId: m_id, currType):
    # verify that the Id isnt already in the environment
    if currId in dict.keys():
        return False

    # if it is a struct, you need to check if all of the subtypes exist (either bool, int, void, or struct in the environment)
    if type(currType) == dict:
        for i in currType.keys():
            # check if it is int, bool, void
            if currType[i] == "int" or "bool" or "void":
                pass
 
            # check if it is an id in the struct environment
            elif currType[i] in globalStructEnvironment:
                pass
            
            # otherwise the type doesnt exist
            else:
                return False

    # add the new id key to the environment wth the type
    typeEnvironment[currId] = currType # in the case of a struct environment you would have a dict for currType

    # return this extended typeEnvironment
    return typeEnvironment



# returns the type from an expression (?) 
# I will call this within the type_check() function to implement return type checking among other things
def getType(statements, localTypeEnvironment):
    # recursively walk through the expression and then return the type when you get to the end
    for i in statements:
        pass
        # consider returning False if you find and error or something

    # once you reach the end, you need to look at the type of the last statment
    else:
        # NEED TO THINK ABOUT WHAT WE DO HERE

    
    #return the type 
    return ...






# CAN A GLOBAL OVERWRITE A STRUCT (vice versa)
# DO WE TRAVERSE GLOBAL OR STRUCT FIRST WHEN LOOKING UP
