from ast_class_definitions import *

def checkReturnTypes(program:m_prog):
    encounteredTypes = {'int':True, 'bool':True}
    for typeDecl in program.types:
        encounteredTypes[typeDecl.id] = True
        for nestedDecl in typeDecl.nested_declarations:
            if nestedDecl.type not in encounteredTypes:
                print(f'ERROR on line {nestedDecl.lineNum}: unrecognized type')
                exit(0)

    for decl in program.global_declarations:
        if decl.type not in encounteredTypes:
            print(f'ERROR on line {decl.lineNum}: unrecognized type')
            exit(0)

    top_env = program.getTopEnv()
    top_type_env = program.getTopTypeEnv()

    for function in program.functions:
        checkFunctionReturn(function, {}, top_env, top_type_env)

def checkFunctionReturn(function:m_function, local_env, top_env, top_type_env):
    for param in function.param_declarations:
        if param.type not in top_type_env:
            print(f'ERROR on line {param.lineNum}: unrecognized type {param.type.type}')
            exit(0)
        local_env[param.id] = (param.lineNum, param.type)

    for decl in function.body_declarations:
        if decl.id in local_env:
            print(f'ERROR on line {decl.lineNum}: local redeclaration of variable {decl.id}')
            exit(0)
        local_env[decl.id] = (decl.lineNum, decl.id)

    for statement in function.statements:
        # ensure all paths through return correct type
        pass

def pathCheck(statement, local_env, top_env, top_type_env):
    match statement:
        case m_bool(val):
            return m_type('bool')

        case m_null():
            return m_type('null')

        case m_num(val):
            return m_type('int')

        case m_id(id):
            if id in local_env:
                id_type = local_env[id][1]
            elif id in top_env:
                id_type = top_env[id][1]
            else:
                print(f'ERROR: undeclared variable: {id}')
                exit(0)

            if id_type in top_type_env:
                return id_type

        case m_assignment(lineNum, target_ids, source_expression):
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
                exit(0)

            # top_type_env is {str : {str : (int, m_type)}}

            for nestedID in target_ids[1:]:
                # if the nested id exists in the type environment
                if nestedID in top_type_env[targetType.identifier]:
                    # reassign target type to the mapped type and continue
                    targetType = top_type_env[targetType.identifier][nestedID]
                else:
                    print(f'ERROR on line {lineNum}: {targetType.identifier}.{nestedID} does not exist')
                    exit(0)
            
            sourceType = pathCheck(source_expression, local_env, top_env, top_type_env)
            if sourceType != targetType:
                print(f'ERROR on line {lineNum}: type mismatch - cannot assign {sourceType.typeID} to {targetType.typeID}')
                exit(0)
                    


        # print → print expression {endl}opt;
        case m_print(lineNum, expression, endl):
            pass

        # conditional → if ( expression ) block {else block}opt
        case m_conditional(lineNum, guard_expression, if_statements, else_statements):
            pass

        # loop → while ( expression ) block
        case m_loop(lineNum, guard_expression, body_statements):
            pass

        # delete → delete expression ;
        case m_delete(expression):
            pass

        # ret → return {expression}opt;
        case m_ret(lineNum, expression):
            pass

        # == != <= < > >= - + * / || &&
        case m_binop(lineNum, operator, left, right):
            pass

        # invocation → id arguments ;
        case m_invocation(lineNum, functionID, args_expressions):
            pass

        # needed whenever using new [struct_id];
        case m_new_struct(struct_id):
            pass

        # unary → {! | −}∗selector
        case m_unary(lineNum, operator, operand_expression):
            pass

