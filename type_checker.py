from re import T
from ast_class_definitions import *

def typeCheckProgram(program:m_prog):
    encounteredTypes = {'int':True, 'bool':True}
    for typeDecl in program.types:
        encounteredTypes[typeDecl.id.identifier] = True
        for nestedDecl in typeDecl.nested_declarations:
            if nestedDecl.type.typeID not in encounteredTypes:
                print(f'ERROR on line {nestedDecl.lineNum}: unrecognized type')
                return -1

    for decl in program.global_declarations:
        if decl.type.typeID not in encounteredTypes:
            print(f'ERROR on line {decl.lineNum}: unrecognized type')
            return -1

    # {str : (int, m_type)}                     map id to type
    top_env = program.getTopEnv()
    # {str : {str : (int, m_type)}}             map struct id to struct contents
    top_type_env = program.getTopTypeEnv()
    top_type_env['int'] = m_type('int')
    top_type_env['bool'] = m_type('int')
    # {str : (int, m_type, list[m_type])}       map function id to (lineNum, retType, argTypes)
    function_env = {}

    for function in program.functions:
        argTypes = [decl.type for decl in function.param_declarations]
        expected = function.return_type
        # add current function to function environment
        function_env[function.id.identifier] = (function.lineNum, expected, argTypes)

        # get return type of statements
        actual = checkFunctionReturn(function, {}, top_env, top_type_env, function_env)
        if actual == -1:
            return -1
        if actual != expected and actual != m_type('null'):
            print(f'ERROR on line {function.lineNum}: expected return type {expected.typeID} not equal to actual return type {actual.typeID}')
            return -1

    return True

def checkFunctionReturn(function:m_function, local_env, top_env, top_type_env, function_env) -> m_type:
    
    # check that all param types are valid
    for param in function.param_declarations:
        if param.type.typeID not in top_type_env:
            print(f'ERROR on line {param.lineNum}: unrecognized type {param.type.typeID}')
            return -1
        local_env[param.id.identifier] = (param.lineNum, param.type)

    # check that there aren't any redeclarations of variables
    for decl in function.body_declarations:
        if decl.id.identifier in local_env:
            print(f'ERROR on line {decl.lineNum}: local redeclaration of variable {decl.id}')
            return -1
        local_env[decl.id.identifier] = (decl.lineNum, decl.type)


    returnType = None
    # get the return type of function body
    for statement in function.statements:
        retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
        if retType == -1:
            return -1

        # to catch the first statement return type
        if returnType == None:
            returnType = retType
        
        # don't care about statements that don't return
        # if the return type of the current statement is not the same
        # as the return type of the previous statement(s), there is an error
        elif retType != None and retType != returnType and (not retType == m_type('null')) and (not returnType == m_type('null')):
            print(f'ERROR in function {function.id}: not all paths return type {returnType.typeID}')
            return -1
    
    # none of the statements in the function return; defaults to void
    if returnType == None:
        returnType = m_type('void')

    return returnType

# returns None when there is an error somewhere
def typeCheck(statement, local_env, top_env, top_type_env, function_env) -> m_type:
    match statement:
        case m_bool():
            return m_type('bool')

        case m_null():
            return m_type('null')

        case m_num() | m_read():
            return m_type('int')

        case m_id():
            lineNum = statement.lineNum
            id = statement.identifier

            # lookup the type of the given id. Check if it was declared before it was accessed
            if id in local_env and local_env[id][0] < lineNum:
                id_type = local_env[id][1]
            elif id in top_env:
                id_type = top_env[id][1]
            else:
                print(f'ERROR: undeclared variable: {id}')
                return -1

            if id_type.typeID in top_type_env:
                return id_type
            else:
                print(f'ERROR: unrecognized type {id_type.typeID}')
                return -1

        case m_assignment():
            lineNum = statement.lineNum
            target_ids = statement.target_ids
            source_expression = statement.source_expression

            targetType = None
            sourceType = None

            id = target_ids[0].identifier
            # if the variable is in the local env, return the mapped type
            # also make sure it was declared before used
            if id in local_env and local_env[id][0] < lineNum:
                targetType = local_env[id][1]
            # if the variable is in the global env, return the mapped type
            # also make sure it was declared before used
            elif id in top_env and top_env[id][0] < lineNum:
                targetType = top_env[id][1]
            else:
                print(f'ERROR on line {lineNum}: undeclared variable {id}')
                return -1

            # top_type_env is {str : {str : (int, m_type)}}

            for nestedID in target_ids[1:]:
                # if the nested id exists in the type environment
                if nestedID.identifier in top_type_env[targetType.typeID]:
                    # reassign target type to the mapped type and continue
                    targetType = top_type_env[targetType.typeID][nestedID.identifier][1]
                else:
                    print(f'ERROR on line {lineNum}: {targetType.typeID}.{nestedID.identifier} does not exist')
                    return -1
            
            sourceType = typeCheck(source_expression, local_env, top_env, top_type_env, function_env)
            if sourceType == -1:
                return -1
            elif sourceType != targetType and targetType != m_type('null') and sourceType != m_type('null'):
            # MADE A CHANGE ON THIS LINE - RILEY (I couldnt print out sourceType.typeID)
                print(f'ERROR on line {lineNum}: type mismatch - cannot assign {sourceType} to {targetType.typeID}')
                return -1  

            return None


        case m_delete():
            exprType = typeCheck(statement.expression, local_env, top_env, top_type_env, function_env)

            if exprType == -1:
                return -1
            elif exprType.typeID == 'int' or exprType.typeID == 'bool' or exprType.typeID == 'null':
                print(f'ERROR on line {statement.lineNum}: cannot delete a non-dynamically-allocated type {exprType.typeID}')
                return -1
            return None


        # print → print expression {endl}opt;
        case m_print():
            lineNum = statement.lineNum
            expression = statement.expression

            exprType = typeCheck(expression, local_env, top_env, top_type_env, function_env)
            # assume you can't print structs; you can only print bool, int, or null
            # MADE A CHANGE ON THIS LINE - RILEY (you can only print int. Also, the printed type is ugly now)
            if exprType == -1:
                return -1
            elif exprType != m_type('int'):
                print(f'ERROR on line {lineNum}: cannot print type {exprType}')
                return -1
            return None

        # conditional → if ( expression ) block {else block}opt
        case m_conditional():
            lineNum = statement.lineNum
            guard_expression = statement.guard_expression
            if_statements = statement.if_statements
            else_statements = statement.else_statements

            guardType = typeCheck(guard_expression, local_env, top_env, top_type_env, function_env)
            if guardType == -1:
                return -1

            if guardType != m_type('bool'):
                print(f'ERROR on line {lineNum}: guard statement evaluated to {guardType} not bool')
                return -1

            ifReturnType = None
            for statement in if_statements:
                # type check all the statements, but if one of them returns, take the first return statement
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if retType == -1:
                    return -1
                if ifReturnType == None:
                    ifReturnType = retType
                elif retType != None and retType != ifReturnType:
                    print(f'ERROR in conditional {lineNum}: body has more than 1 possible return type')
                    return -1

            if else_statements[0] == None:
                return ifReturnType

            elseReturnType = None
            for statement in else_statements:
                # type check all the statements, but if one of them returns, take the first return statement
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if retType == -1:
                    return -1
                elif elseReturnType == None:
                    elseReturnType = retType
                elif retType != None and retType != elseReturnType:
                    print(f'ERROR in conditional {lineNum}: body has more than 1 possible return type')
                    return -1
            
            # if both return types are the same, if statement will always return the same
            if ifReturnType == elseReturnType or ifReturnType == m_type('null') or elseReturnType == m_type('null'):
                return ifReturnType
            
            print(f'ERROR in if statement on line {lineNum}: if and else return types are different. {ifReturnType} and {elseReturnType}')
            return -1

        # loop → while ( expression ) block
        case m_loop():
            lineNum = statement.lineNum
            guard_expression = statement.guard_expression
            body_statements = statement.body_statements

            guardType = typeCheck(guard_expression, local_env, top_env, top_type_env, function_env)
            if guardType == -1:
                return -1

            if guardType != m_type('bool'):
                print(f'ERROR on line {lineNum}: guard statement evaluated to {guardType} not bool')
                return -1

            returnType = None
            for statement in body_statements:
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if retType == -1:
                    return -1
                elif returnType == None:
                    returnType = retType
                elif retType != None and retType != returnType:
                    print(f'ERROR in while loop {lineNum}: body has more than 1 possible return type')
                    return -1

            return returnType

        # delete → delete expression ;
        case m_delete():
            expression = statement.expression
            exprType = typeCheck(expression)
            if exprType == -1:
                return -1
            if exprType not in top_type_env:
                print(f'ERROR on line {expression.lineNum}: given type {exprType} is not a struct')
                return -1
            return None

        # ret → return {expression}opt;
        case m_ret():
            lineNum = statement.lineNum
            expression = statement.expression

            if expression == None:
                return m_type('void')
            
            return typeCheck(expression, local_env, top_env, top_type_env, function_env)

        # == != <= < > >= - + * / || &&
        case m_binop():
            lineNum = statement.lineNum
            operator = statement.operator
            left = statement.left_expression
            right = statement.right_expression

            match operator:
                case '==' | '!=':
                    return m_type('bool')
                case '<=' | '<' | '>=' | '>':
                    leftType = typeCheck(left, local_env, top_env, top_type_env, function_env)
                    rightType = typeCheck(right, local_env, top_env, top_type_env, function_env)
                    if leftType == -1 or rightType == -1:
                        return -1
                    if leftType == rightType and leftType == m_type('int'):
                        return m_type('bool')
                case '-' | '+' | '*' | '/':
                    leftType = typeCheck(left, local_env, top_env, top_type_env, function_env)
                    rightType = typeCheck(right, local_env, top_env, top_type_env, function_env)
                    if leftType == -1 or rightType == -1:
                        return -1
                    if leftType == rightType and leftType == m_type('int'):
                        return m_type('int')
                case '||' | '&&':
                    leftType = typeCheck(left, local_env, top_env, top_type_env, function_env)
                    rightType = typeCheck(right, local_env, top_env, top_type_env, function_env)
                    if leftType == -1 or rightType == -1:
                        return -1
                    if leftType == rightType and leftType == m_type('bool'):
                        return m_type('bool')                    
                case _:
                    print(f'ERROR on line {lineNum}: unrecognized binop {operator}')
                    return -1

        # invocation → id arguments ;
        case m_invocation():
            lineNum = statement.lineNum
            functionID = statement.id
            args_expressions = statement.args_expressions

            if functionID.identifier in function_env:
                actualArgTypes = [typeCheck(expr, local_env, top_env, top_type_env, function_env) for expr in args_expressions]
                if -1 in actualArgTypes:
                    return -1

                # if all the parameter types are equal to expected arg types, return the function's return type
                if function_env[functionID.identifier][2] == actualArgTypes:
                    return function_env[functionID.identifier][1]
                else:
                    print(f'ERROR on line {lineNum}: mismatched argument types')
                    return -1
            else:
                print(f'ERROR on line {lineNum}: unrecognized function {functionID.identifier}')
                return -1

        # needed whenever using new [struct_id];
        case m_new_struct():
            struct_id = statement.struct_id

            if struct_id.identifier not in top_type_env:
                print(f'ERROR: unrecognized struct id {struct_id.identifier}')
                return -1
            
            return m_type(struct_id.identifier)

        # unary → {! | −}∗selector
        case m_unary():
            lineNum = statement.lineNum
            operator = statement.operator
            operand_expression = statement.operand_expression

            # MADE A CHANGE ON THIS LINE - RILEY (previously you just had: typeCheck(operand_expression) )
            operandType = typeCheck(operand_expression, local_env, top_env, top_type_env, function_env)
            if operandType == -1:
                return -1
            match operator:
                case '!':
                    if operandType != m_type('bool'):
                        print(f'ERROR on line {lineNum}: invalid operand type for operator ! -- expected bool, got {operandType.typeID}')
                        return -1
                    return m_type('bool')
                case '-':
                    if operandType != m_type('int'):
                        print(f'ERROR on line {lineNum}: invalid operand type for operator "-" -- expected int, got {operandType.typeID}')
                        return -1
                    return m_type('int')
                case _:
                    print(f'ERROR on line {lineNum}: unrecognized operator {operator}')
                    return -1
        
        case m_dot():
            lineNum = statement.lineNum
            ids = statement.ids


            currentType = None
            id = ids[0].identifier
            # if the variable is in the local env, return the mapped type
            if id in local_env and local_env[id][0] < lineNum:
                currentType = local_env[id][1]
            # if the variable is in the global env, return the mapped type
            elif id in top_env and top_env[id][0] < lineNum:
                currentType = top_env[id][1]
            else:
                print(f'ERROR on line {lineNum}: undeclared variable {id}')
                return -1

            if len(ids) == 1:
                return currentType
            return typeCheckDot(top_type_env, ids[1:], currentType)

        case other:
            print(f"ERROR: unrecognized structure in AST \n{other}")

# top_type_env is {str : {str : (int, m_type)}}
def typeCheckDot(type_env:dict, ids:list[m_id], currentType:m_type):
    if currentType.typeID not in type_env:
        print(f'ERROR: unrecognized type {currentType.typeID}')
        return -1
    elif ids[0].identifier not in type_env[currentType.typeID]:
        print(f'ERROR on line {ids[0].lineNum}: {currentType.typeID}.{ids[0].identifier} does not exist')
        return -1
    elif len(ids) == 1:
        return type_env[currentType.typeID][ids[0].identifier][1]
    else:
        return typeCheckDot(type_env, ids[1:], type_env[currentType.typeID][ids[0].identifier][1])