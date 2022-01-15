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
            types = parseTypes(json['types'])
            declarations = parseDeclarations(json['declarations'])
            functions = parseFunctions(json['functions'])
            return m_prog(types, declarations, functions)

        case {'line':_,'id':_,'fields':_}:
            # check if id is protected keyword?
            m_decls = []
            for type_decl in json['fields']:
                m_decls.append(parse(type_decl))
            return m_type_declaration(m_id(json['id']), m_declarations(m_decls))

        case {'line':_,'type':_,'id':_}:
            return m_declaration(parse(json['type']), parse(json['id']))

        case {'line':_, 'exp':'binary', 'operator':_, 'lft':_, 'rht':_}:
            return m_binop(json['operator'], parse(json['lft']), parse(json['rht']))

        case {'line':_, 'exp':'id', 'id':_}:
            return m_id(json['id'])
        
        case {'line':_, 'exp':'num', 'value':_}:
            return m_num(int(json['value']))

        case {'line':_, 'exp':'true' | 'false'}:
            return m_bool(bool(json['exp']))

        case {'line':_, 'stmt':'return', 'exp':_}:
            return m_statement(m_ret(parse(json['exp'])))

        case {'line':_, 'stmt':'print', 'exp':_, 'endl':_}:
            return m_statement(m_print(parse(json['exp']), bool(json['endl'])))

        case {'line':_, 'stmt':'assign', 'source':_, 'target':_}:
            target = m_lvalue(parse(json['target']))
            return m_statement(m_assignment(target, parse(json['source'])))

        case {'line':_, 'stmt':'while', 'guard':_, 'body':_}:
            return m_statement(m_loop(parse(json['guard']), parse(json['body'])))
        
        case {'line':_, 'stmt':'if', 'guard':_, 'then':_}:
            return m_statement(m_conditional(parse(json['guard']), parse(json['then'])))

        case {'stmt':'block', 'list':_}:
            statements = []
            for stmt in json['list']:
                statements.append(parse(stmt))
            return m_block(m_statement_list(statements))

        case {'line':_, 'left':_, 'id':_}:
            # expects parent struct recursive parse to go to this or previous case
            parentStruct = parse(json['left'])
            parentStruct.append(m_id(json['id']))
            return parentStruct

        case {'line':_, 'id':_}:
            # TODO handle the case where id is a struct and assigning to value within the struct
            # ex: A.j = 5
            return [m_id(json['id'])]


        case 'int':
            return m_type('int')

        case 'bool':
            return m_type('bool')

        case other:
            if type(other) == int:
                return m_num(other)
            elif type(other) == bool:
                return m_bool(other)
            else:
                return m_id(other)

def parseDeclarations(json):
    dcls = []
    for decl in json:
        dcls.append(parse(decl))
    return m_declarations(dcls)

def parseTypes(json):
    type_declarations = []
    for type_decl in json:
        type_declarations.append(parse(type_decl))
    return m_types(type_declarations)

def parseFunctions(json):
    funs = []
    for fun in json:
        id = m_id(fun['id'])
        parameters = parseDeclarations(fun['parameters'])
        returnType = m_type(fun['return_type'])
        declarations = parseDeclarations(fun['declarations'])

        body = []
        for block in fun['body']:
            body.append(parse(block))
        
        funs.append(m_function(id, parameters, returnType, declarations, m_statement_list(body)))
    return m_functions(funs)



# print("")
# with open("test.json") as jsonFile:
#     jsonContents = json.load(jsonFile)
#     parseJson(jsonContents)

        # # # m_type (struct)
        # # case _: # THIS ONE CANT REALLY BE RIGHT
        # #     # type = m_type()
        # #     print("MATCHED")

        # # COME BACK TO THIS
        # # m_id_list 
        # case {'id': _ }:
        #     # id_list = m_id_list()
        #     print("MATCHED")

        # # good?
        # # m_declaration 
        # case {'type':_,'id':_,'list':_}:
        #     # declaration = m_declaration()
        #     print("MATCHED")

        # # SHOULD BE JUST 1 OR MORE m_declaration. NOT SURE HOW TO DO THAT YET
        # # m_declarations 
        # case {'type':_,'id':_,'list':_} : # maybe something like this??
        #     # declarations = m_declarations()
        #     print("MATCHED")

        # # NO CLUE HERE
        # # m_nested_decl → decl ; {decl ;}∗
        # case {'line':_,'type':_,'id':_}:
        #     # nested_decl = m_nested_decl()
        #     print("MATCHED")

        # # good?
        # # m_type_declaration → struct id { nested decl } ;
        # case {'line':_,'id':_,'fields':[_]}:
        #     # type_declaration = m_type_declaration()
        #     print("MATCHED")

        # # 0 or more m_type_declaration, still dont know how to do that
        # # m_types → {type declaration}∗
        # case [{"line":_,"id":_,"fields":_}]: # this * is wrong
        #     # types = m_types()
        #     print("MATCHED")

        # case _:
        #     print("FAILED")
