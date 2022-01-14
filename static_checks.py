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
def type_check(expression ,typeEnvironment: dict):
    # step through each expression 
    expressionType = type(expression)

    # MAKE SURE THIS BRANCH RETURNS True OR False INSTEAD OF THE ENVIRONMENT
    # m_prog 
    if expressionType is m_prog:
        # self.types = types
        # self.declarations = declarations
        # self.functions = functions

        print("MATCHED")


    # # m_decl 
    # elif expressionType is m_decl:
    #     print("MATCHED")


    # m_type
    elif expressionType is m_type:
        print("MATCHED")
        if expression.type == "int" or expression.type == "bool" or expression.type in typeEnvironment:
            # GREAT SUCCESS
            # return True
            return typeEnviroment # returning environment instead of True
        else:
            # failure, how do we want to return?
            return False



    # # m_id_list → id {,id}∗
    # elif expressionType is m_id_list:
    #     print("MATCHED")
    #     for i in expression.id_list:
    #         if i == "int" or i == "bool" or i in typeEnvironment:
    #             continue
    #         else:
    #             return False


    # ADD SOMETHING TO THE ENVIRONMENT
    # m_declaration 
    elif expressionType is m_declaration:
        print("MATCHED")
        # check that the type is valid
        typeEnvironment = type_check(expression.type, typeEnvironment)
        # type_check(expression.type, typeEnvironment)
        
        # WHICH LINE IS CORRECT?? I THINK I NEED TO UPDATE typeEnvironment but Im not certain

        # extend the environment to have the id-type mapping
        return extendEnv(typeEnviroment, expression.id, expression.type) # DOUBLE CHECK THIS LINE
        



    # ADD SOMETHING TO THE ENVIRONMENT
    # m_declarations 
    elif expressionType is m_declarations:
        print("MATCHED")
        # YOU SHOULD UPDATE THE ENVIRONMENT AS YOU STEP THROUGH THE declarations
        # EACH ONE NEEDS TO HAVE THE UPDATES FROM THE PREVIOUS ONE
        for i in expression.declarations:


            



    # m_nested_decl → decl ; {decl ;}∗
    elif expressionType is m_nested_decl:
        print("MATCHED")


    # m_type_declaration → struct id { nested decl } ;
    elif expressionType is m_type_declarations:
        print("MATCHED")


    # m_types → {type declaration}∗
    elif expressionType is m_types:
        print("MATCHED")


    # m_parameters 
    elif expressionType is m_parameters:
        print("MATCHED")


    # m_return_type
    elif expressionType is m_return_type:
        print("MATCHED")


    # ADD SOMETHING TO THE ENVIRONMENT
    # m_function 
    elif expressionType is m_function:
        print("MATCHED")


    # ADD SOMETHING TO THE ENVIRONMENT
    # m_functions 
    elif expressionType is m_functions:
        print("MATCHED")


    # m_assignment 
    elif expressionType is m_assignment:
        print("MATCHED")


    # m_print 
    elif expressionType is m_print:
        print("MATCHED")


    # m_conditional
    elif expressionType is m_conditional:
        print("MATCHED")


    # m_loop 
    elif expressionType is m_loop:
        print("MATCHED")


    # m_delete 
    elif expressionType is m_delete:
        print("MATCHED")


    # m_ret 
    elif expressionType is m_ret:
        print("MATCHED")


    # m_invocation 
    elif expressionType is m_invocation:
        print("MATCHED")

        
    # m_statement 
    elif expressionType is m_statement:
        print("MATCHED") 


    # m_statement_list 
    elif expressionType is m_statement_list:
        print("MATCHED")


    # m_block 
    elif expressionType is m_block:
        print("MATCHED")


    # m_lvalue 
    elif expressionType is m_lvalue:
        print("MATCHED")


    # m_expression
    elif expressionType is m_expression:
        print("MATCHED")


    # m_boolterm 
    elif expressionType is m_boolterm:
        print("MATCHED")


    # m_eqterm 
    elif expressionType is m_eqterm:
        print("MATCHED")


    # m_relterm 
    elif expressionType is m_relterm:
        print("MATCHED")


    # m_simple 
    elif expressionType is m_simple:
        print("MATCHED")


    # m_term 
    elif expressionType is m_term:
        print("MATCHED")


    # m_unary 
    elif expressionType is m_unary:
        print("MATCHED")


    # m_selector 
    elif expressionType is m_selector:
        print("MATCHED")



    # m_factor  _(expression)_
    elif expressionType is m_factor:
        print("MATCHED")



    # m_arguments
    elif expressionType is m_arguments:
        print("MATCHED")


    else:
        print("FAILED TO RECOGNIZE TYPE")
        return False






def extendEnv(typeEnvironment: dict, currId: m_id, currType: m_type):
    # add the new id key to the environment wth the value m_type
