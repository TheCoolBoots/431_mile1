from ast_class_definitions import *

def checkReturnTypes(program:m_prog):
    top_env = program.getTopEnv()
    top_type_env = program.getTopTypeEnv()

    for function in program.functions:
        checkFunctionReturn(function, {}, top_env, top_type_env)

def checkFunctionReturn(function:m_function, local_env, top_env, top_type_env):
    pass