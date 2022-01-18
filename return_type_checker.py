from re import T
from ast_class_definitions import *

def checkReturnTypes(program:m_prog):
    encounteredTypes = {'int':True, 'bool':True}
    for typeDecl in program.types:
        encounteredTypes[typeDecl.id.identifier] = True
        for nestedDecl in typeDecl.nested_declarations:
            if nestedDecl.type not in encounteredTypes:
                print(f'ERROR on line {nestedDecl.lineNum}: unrecognized type')
                return None

    for decl in program.global_declarations:
        if decl.type not in encounteredTypes:
            print(f'ERROR on line {decl.lineNum}: unrecognized type')
            return None

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
        function_env[function.id.identifier] = (function.lineNum, expected, argTypes)
        actual = checkFunctionReturn(function, {}, top_env, top_type_env, function_env)
        if actual != expected:
            print(f'ERROR on line {function.lineNum}: expected return type {expected.typeID} not equal to actual return type {actual.typeID}')
            return None

    return True

def checkFunctionReturn(function:m_function, local_env, top_env, top_type_env, function_env) -> m_type:
    for param in function.param_declarations:
        if param.type not in top_type_env:
            print(f'ERROR on line {param.lineNum}: unrecognized type {param.type.typeID}')
            return None
        local_env[param.id] = (param.lineNum, param.type)

    for decl in function.body_declarations:
        if decl.id in local_env:
            print(f'ERROR on line {decl.lineNum}: local redeclaration of variable {decl.id}')
            return None
        local_env[decl.id] = (decl.lineNum, decl.id)

    found = False
    returnType = m_type('void')
    for statement in function.statements:
        retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
        if not found and retType != m_type('void'):
            returnType = retType
            found = True
    
    return returnType


def typeCheck(statement, local_env, top_env, top_type_env, function_env) -> m_type:
    match statement:
        case m_bool():
            return m_type('bool')

        case m_null():
            return m_type('null')

        case m_num():
            return m_type('int')

        case m_id():
            lineNum = statement.lineNum
            id = statement.identifier

            # lookup the type of the given id
            if id in local_env and local_env[id][0] < lineNum:
                id_type = local_env[id][1]
            elif id in top_env:
                id_type = top_env[id][1]
            else:
                print(f'ERROR: undeclared variable: {id}')
                return None

            if id_type.typeID in top_type_env:
                return id_type

        case m_assignment():
            lineNum = statement.lineNum
            target_ids = statement.target_ids
            source_expression = statement.source_expression

            targetType = None
            sourceType = None

            id = target_ids[0].identifier
            # if the variable is in the local env, return the mapped type
            if id in local_env and local_env[id][0] < lineNum:
                targetType = local_env[id][1]
            # if the variable is in the global env, return the mapped type
            elif id in top_env and top_env[id][0] < lineNum:
                targetType = top_env[id][1]
            else:
                print(f'ERROR on line {lineNum}: undeclared variable {id}')
                return None

            # top_type_env is {str : {str : (int, m_type)}}

            for nestedID in target_ids[1:]:
                # if the nested id exists in the type environment
                if nestedID.identifier in top_type_env[targetType.typeID]:
                    # reassign target type to the mapped type and continue
                    targetType = top_type_env[targetType.typeID][nestedID.identifier]
                else:
                    print(f'ERROR on line {lineNum}: {targetType.typeID}.{nestedID.identifier} does not exist')
                    return None
            
            sourceType = typeCheck(source_expression, local_env, top_env, top_type_env, function_env)
            if sourceType != targetType:
                print(f'ERROR on line {lineNum}: type mismatch - cannot assign {sourceType.typeID} to {targetType.typeID}')
                return None  

            return m_type('void') 


        # print → print expression {endl}opt;
        case m_print():
            lineNum = statement.lineNum
            expression = statement.expression

            exprType = typeCheck(expression, local_env, top_env, top_type_env, function_env)
            if exprType not in [m_type('int'), m_type('bool'), m_type('null')]:
                print(f'ERROR on line {lineNum}: cannot print type {exprType.typeID}')
            return m_type('void')

        # conditional → if ( expression ) block {else block}opt
        case m_conditional():
            lineNum = statement.lineNum
            guard_expression = statement.guard_expression
            if_statements = statement.if_statements
            else_statements = statement.else_statements


            guardType = typeCheck(guard_expression, local_env, top_env, top_type_env, function_env)

            if guardType != m_type('bool'):
                print(f'ERROR on line {lineNum}: guard statement evaluated to {guardType.typeID} not bool')
                return None

            found = False
            ifReturnType = m_type('void')
            for statement in if_statements:
                # type check all the statements, but if one of them returns, take the first return statement
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if not found and retType != m_type('void'):
                    ifReturnType = retType
                    found = True

            found = False
            elseReturnType = m_type('void')
            for statement in else_statements:
                # type check all the statements, but if one of them returns, take the first return statement
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if not found and retType != m_type('void'):
                    elseReturnType = retType
                    found = True
            
            # if both return types are the same, if statement will always return the same
            if ifReturnType == elseReturnType:
                return ifReturnType
            
            print(f'ERROR in if statement on line {lineNum}: if and else return types are different. {ifReturnType.typeID} and {elseReturnType.typeID}')
            return None

        # loop → while ( expression ) block
        case m_loop():
            lineNum = statement.lineNum
            guard_expression = statement.guard_expression
            body_statements = statement.body_statements

            guardType = typeCheck(guard_expression, local_env, top_env, top_type_env, function_env)

            if guardType != m_type('bool'):
                print(f'ERROR on line {lineNum}: guard statement evaluated to {guardType.typeID} not bool')
                return None

            found = False
            returnType = m_type('void')
            for statement in body_statements:
                retType = typeCheck(statement, local_env, top_env, top_type_env, function_env)
                if not found and retType != m_type('void'):
                    returnType = retType
                    found = True

            return returnType

        # delete → delete expression ;
        case m_delete():
            expression = statement.expression

            return typeCheck(expression)

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
                    if leftType == rightType and leftType == m_type('int'):
                        return m_type('bool')
                case '-' | '+' | '*' | '/':
                    leftType = typeCheck(left, local_env, top_env, top_type_env, function_env)
                    rightType = typeCheck(right, local_env, top_env, top_type_env, function_env)
                    if leftType == rightType and leftType == m_type('int'):
                        return m_type('int')
                case '||' | '&&':
                    leftType = typeCheck(left, local_env, top_env, top_type_env, function_env)
                    rightType = typeCheck(right, local_env, top_env, top_type_env, function_env)
                    if leftType == rightType and leftType == m_type('bool'):
                        return m_type('bool')                    
                case _:
                    print(f'ERROR on line {lineNum}: unrecognized binop {operator}')
                    return None

        # invocation → id arguments ;
        case m_invocation():
            lineNum = statement.lineNum
            functionID = statement.id
            args_expressions = statement.args_expressions


            if functionID.identifier in function_env:
                actualArgTypes = [typeCheck(expr) for expr in args_expressions]
                if listsEqual(function_env[functionID.identifier][2], actualArgTypes):
                    return function_env[functionID.identifier][1]
                else:
                    print(f'ERROR on line {lineNum}: mismatched argument types')
                    return None
            else:
                print(f'ERROR on line {lineNum}: unrecognized function {functionID.identifier}')

        # needed whenever using new [struct_id];
        case m_new_struct():
            struct_id = statement.struct_id

            if struct_id.identifier not in top_type_env:
                print(f'ERROR: unrecognized struct id {struct_id.identifier}')
            
            return m_type(struct_id.identifier)

        # unary → {! | −}∗selector
        case m_unary():
            lineNum = statement.lineNum
            operator = statement.operator
            operand_expression = statement.operand_expression


            operandType = typeCheck(operand_expression)
            match operator:
                case '!':
                    if operandType != m_type('bool'):
                        print(f'ERROR on line {lineNum}: invalid operand type for operator ! -- expected bool, got {operandType.typeID}')
                        return None
                    return m_type('bool')
                case '-':
                    if operandType != m_type('int'):
                        print(f'ERROR on line {lineNum}: invalid operand type for operator "-" -- expected int, got {operandType.typeID}')
                        return None
                    return m_type('int')
                case _:
                    print(f'ERROR on line {lineNum}: unrecognized operator {operator}')
                    return None
        
        case m_dot():
            lineNum = statement.lineNum
            ids = statement.ids


            targetType = None
            id = ids[0].identifier
            # if the variable is in the local env, return the mapped type
            if id in local_env and local_env[id][0] < lineNum:
                targetType = local_env[id][1]
            # if the variable is in the global env, return the mapped type
            elif id in top_env and top_env[id][0] < lineNum:
                targetType = top_env[id][1]
            else:
                print(f'ERROR on line {lineNum}: undeclared variable {id}')
                return None

            # top_type_env is {str : {str : (int, m_type)}}

            for nestedID in ids[1:]:
                # if the nested id exists in the type environment
                if nestedID in top_type_env[targetType.identifier]:
                    # reassign target type to the mapped type and continue
                    targetType = top_type_env[targetType.identifier][nestedID]
                else:
                    print(f'ERROR on line {lineNum}: {targetType.identifier}.{nestedID} does not exist')
                    return None

            return targetType