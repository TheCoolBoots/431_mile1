# import pandas as pd
# import numpy as np
import json
from ast_class_definitions import *

"""
TASK 2: recursively parse json file into python classes
    should return a m_program object
    pattern match at each level of json file: https://www.python.org/dev/peps/pep-0636/
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""

def parse(json):
    match json:
        case {'types':_,'declarations':_,'functions':_}:
            types = [parse(type_decl) for type_decl in json['types']]
            declarations = [parse(declaration) for declaration in json['declarations']]
            functions = [parse(func) for func in json['functions']]
            return m_prog(types, declarations, functions)

        case {'line':_, 'id':_, 'parameters':_, 'return_type':_, 'declarations':_, 'body':_}:
            params = [parse(param) for param in json['parameters']]
            decls = [parse(declaration) for declaration in json['declarations']]
            body = [parse(statement) for statement in json['body']]
            return m_function(int(json['line']), m_id(json['line'], json['id']), params, m_type(json['return_type']), decls, body)

        case {'line':_, 'exp':'binary', 'operator':_, 'lft':_, 'rht':_}:
            return m_binop(int(json['line']), json['operator'], parse(json['lft']), parse(json['rht']))

        case {'line':_, 'exp':'id', 'id':_}:
            return m_id(json['line'], json['id'])
        
        case {'line':_, 'exp':'num', 'value':_}:
            return m_num(int(json['value']))

        case {'line':_, 'exp':'true' | 'false'}:
            return m_bool(bool(json['exp']))
        
        case {'line':_, 'exp':'null'}:
            return m_null()

        case {'line':lineNum, 'exp':'read'}:
            return m_read(lineNum)

        case {'line':_, 'exp':'invocation', 'id':_, 'args':_}:
            args = [parse(arg) for arg in json['args']]
            return m_invocation(int(json['line']), m_id(json['line'], json['id']), args)

        case {'line':_, 'exp':'dot', 'left':_, 'id':_}:
            parentStruct = parse(json['left'])
            if type(parentStruct) == list:
                parentStruct.append(m_id(json['line'], json['id']))
                return parentStruct
            else:
                return [parentStruct, m_id(json['line'], json['id'])]

        case {'line':_, 'exp':'new', 'id':_}:
            return m_new_struct(m_id(json['line'], json['id']))

        case {'line':_, 'exp':'unary', 'operator':_, 'operand':_}:
            return m_unary(int(json['line']), json['operator'], parse(json['operand']))

        case {'line':_, 'stmt':'return', 'exp':_}:
            return m_ret(int(json['line']), parse(json['exp']))

        case {'line':_, 'stmt':'return'}:
            return m_ret(int(json['line']), None)

        case {'line':_, 'stmt':'delete', 'exp':expression}:
            return m_delete(parse(expression))

        case {'line':_, 'stmt':'print', 'exp':_, 'endl':_}:
            return m_print(int(json['line']), parse(json['exp']), bool(json['endl']))

        case {'line':_, 'stmt':'assign', 'source':_, 'target':_}:
            target = parse(json['target'])
            return m_assignment(int(json['line']), target, parse(json['source']))

        case {'line':_, 'stmt':'while', 'guard':_, 'body':_}:
            return m_loop(int(json['line']), parse(json['guard']), parse(json['body']))    

        case {'line':_, 'stmt':'if', 'guard':_, 'then':_, 'else':_}:
            return m_conditional(int(json['line']), parse(json['guard']), parse(json['then']), parse(json['else']))
        
        case {'line':_, 'stmt':'if', 'guard':_, 'then':_}:
            return m_conditional(int(json['line']), parse(json['guard']), parse(json['then']))

        case {'stmt':'block', 'list':_}:
            return [parse(statement) for statement in json['list']]

        case {'line':_, 'left':_, 'id':_}:
            parentStruct = parse(json['left'])
            if type(parentStruct) == list:
                parentStruct.append(m_id(json['line'], json['id']))
                return parentStruct
            else:
                return [parentStruct, m_id(json['line'], json['id'])]

        case {'line':_,'id':_,'fields':_}:
            # check if id is protected keyword?
            m_decls = [parse(type_decl) for type_decl in json['fields']]
            return m_type_declaration(int(json['line']), m_id(json['line'], json['id']), m_decls)

        case {'line':_,'type':_,'id':_}:
            return m_declaration(int(json['line']), m_type(json['type']), m_id(json['line'], json['id']))

        case {'line':_, 'id':_}:
            # TODO handle the case where id is a struct and assigning to value within the struct
            # ex: A.j = 5
            
            return [m_id(json['line'], json['id'])]


        case _:
            print(f'unrecognized structure: {json}')

