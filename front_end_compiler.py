# import pandas as pd
# import numpy as np
import json


class m_expression:
    None
class m_block:
    None
class m_arguments:
    None
class m_lvalue:
    None

"""
TASK 1: create python class for each format as described in overview.pdf
    name class m_[name of thing]
    ex def m_program(types declarations functions)
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""


class m_id:
    def __init__(self, identifier:str):
      self.identifier = identifier

# type → int | bool | struct id
class m_type:
    def __init__(self, typeID:str):
        self.type = typeID
    def __init__(self, typeID:m_id):
        self.type = typeID

# decl → type id
class m_decl:
    def __init__(self, type:m_type, id:m_id):
      self.type = type
      self.id = id

# id list → id {,id}∗
class m_id_list:
    def __init__(self, id_list:list[m_id]):
        self.id_list = id_list # TODO check id_list len >= 1
        if len(self.id_list < 1):
            print("ERROR: according to overview.pdf, an id_list should have 1 or more ids. This condition is not met somewhere")

# declaration → type id list ;
class m_declaration:
    def __init__(self, type:m_type, id_list:m_id_list):
        self.type = type
        self.id_list = id_list

# declarations → {declaration}∗
class m_declarations:
    def __init__(self, declarations:list[m_declaration]):
      self.declarations = declarations

# nested decl → decl ; {decl ;}∗
class m_nested_decl:
    def __init__(self, declarations:list[m_decl]):
      self.declarations = declarations  # TODO check declarations len >= 1
      if len(self.declarations < 1):
            print(f"ERROR: according to overview.pdf, a nested_decl should have 1 or more ids. This condition is not met somewhere")

# type declaration → struct id { nested decl } ;
class m_type_declaration:
    def __init__(self, id:m_id, nested_decl:m_nested_decl):
        self.id = id
        self.nested_decl = nested_decl

# types → {type declaration}∗
class m_types:
    def __init__(self, type_declarations:list[m_type_declaration]):
        self.type_declarations = type_declarations

# parameters → ( {decl {,decl}∗}opt)
class m_parameters:
    def __init__(self, decls:list[m_decl] = None):
        self.decls = decls  # TODO if decls != None, len needs to be >= 1
        if(self.decls != None and len(decls) < 1):
            print(f"ERROR: according to overview.pdf, a paramaters should have 1 or more decls. This condition is not met somewhere")

# return type → type | void
class m_return_type:
    def __init__(self, type:m_type):
        self.type = type
    def __init__(self, type:str):
        self.type = type    # TODO check if return val is "void"
        if(self.type != "void"):
            print(f'ERROR: the return type should either be a valid type or void.')

# function → fun id parameters return type { declarations statement list }
class m_function:
    def __init__(self, id:m_id, parameters:m_parameters, return_type:m_return_type, declarations:m_declarations, statement_list):
        self.id = id
        self.parameters = parameters
        self.return_type = return_type
        self.declarations = declarations
        self.statement_list = statement_list

# functions → {function}∗
class m_functions:
    def __init__(self, functions:list[m_function]):
      self.functions = functions

# program → types declarations functions
class m_prog:
    def __init__(self, types:m_types, declarations:m_declarations, functions:m_functions):
        self.types = types
        self.declarations = declarations
        self.functions = functions

# assignment → lvalue = { expression | read } ;
class m_assignment:
    def __init__(self, lvalue:m_lvalue, assignmentVal:m_expression):
        self.lvalue = lvalue
        self.assignmentVal = assignmentVal
    def __init__(self, lvalue:m_lvalue, assignmentVal:str):
        self.lvalue = lvalue
        self.assignmentVal = assignmentVal # check if assignmentVal is "read"
        if self.assignmentVal != 'read':
            print('ERROR: the right side of an assignment should either parse to an expression or "read"')

# print → print expression {endl}opt;
class m_print:
    def __init__(self, expression:m_expression, endl:bool = None):
        self.expression = expression
        self.endl = endl

# conditional → if ( expression ) block {else block}opt
class m_conditional:
    def __init__(self, expression:m_expression, ifBlock:m_block, elseBlock:m_block = None):
        self.expression = expression
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

# loop → while ( expression ) block
class m_loop:
    def __init__(self, expression:m_expression, block:m_block):
        self.expression = expression
        self.block = block

# delete → delete expression ;
class m_delete:
    def __init__(self, expression:m_expression):
      self.expression = expression

# ret → return {expression}opt;
class m_ret:
    def __init__(self, expression:m_expression = None):
        self.expression = expression

# invocation → id arguments ;
class m_invocation:
    def __init__(self, id:m_id, arguments:m_arguments):
        self.id = id
        self.arguments = arguments

# statement → block | assignment | print | conditional | loop | delete | ret | invocation
class m_statement:
    def __init__(self, contents:m_block): #  NOTE cyclical definition statement -> block -> statement list -> statement
        self.contents = contents
    def __init__(self, contents:m_assignment):
        self.contents = contents
    def __init__(self, contents:m_print):
        self.contents = contents
    def __init__(self, contents:m_conditional):
        self.contents = contents
    def __init__(self, contents:m_loop):
        self.contents = contents
    def __init__(self, contents:m_delete):
        self.contents = contents
    def __init__(self, contents:m_ret):
        self.contents = contents
    def __init__(self, contents:m_invocation):
        self.contents = contents

# statement list → {statement}∗
class m_statement_list:
    def __init__(self, statements:list[m_statement]):
        self.statements = statements

# block → { statement list }
class m_block:
    def __init__(self, statement_list:m_statement_list):
        self.statement_list = statement_list

# lvalue → id {.id}∗
class m_lvalue:
    def __init__(self, m_ids:list[m_id]):
        self.m_ids = m_ids  # length of m_ids should be >= 1
        if len(self.m_ids) < 1:
            print(f"ERROR: according to overview.pdf, a lvalue should have 1 or more ids. This condition is not met somewhere")

# ( expression ) | id {arguments}opt| number | true | false | new id | null
class m_factor:
    def __init__(self, contents:m_expression):
        self.expression = contents
    def __init__(self, contents:m_id, arguments:m_arguments = None):
        self.expression = contents
        self.arguments = arguments
    def __init__(self, contents:int):
        self.expression = contents
    def __init__(self, contents:str):
        self.expression = contents  # TODO contents should either be "true", "false", or "null"
        keywords = ['true', 'false', 'null']
        if self.expression not in keywords:
            print(f'ERROR: invalid keyword in m_factor. Got {self.expression} but expected one of {keywords}.')
    def __init__(self, contents:str, id:m_id):  # for the new id case
        self.expression = contents  # TODO contents should be "new"
        if self.expression != "new":
            print(f'ERROR: expected keyword "new" in m_factor but got keyword {self.expression}')
        self.id = id

# selector → factor {.id}∗
class m_selector:
    def __init__(self, factor:m_factor, identifiers:list[m_id]):
        self.factor = factor
        self.identifiers = identifiers

# unary → {! | −}∗selector
class m_unary:
    def __init__(self, operators:list[str], selector:m_selector):
        self.operators = operators
        self.selector = selector

# term → unary {{∗ | /} unary}∗
class m_term:
    def __init__(self, unarys:list[m_unary], operators:list[str]):
        self.unarys = unarys
        self.operators = operators

# simple → term {{+ | −} term}∗
class m_simple:
    def __init__(self, terms:list[m_term], operators:list[str]):
        self.terms = terms
        self.operators = operators

# relterm → simple {{<| >| <= | >=} simple}∗
class m_relterm:
    def __init__(self, simples:list[m_simple], operators:list[str]):
        self.simples = simples
        self.operators = operators

# eqterm → relterm {{== | ! =} relterm}∗
class m_eqterm:
    def __init__(self, relterms:list[m_relterm], operators:list[str]):
        self.relterms = relterms
        self.operators = operators

# boolterm → eqterm {&& eqterm}∗
class m_boolterm:
    def __init__(self, eqterms:list[m_eqterm]):
        self.eqterms = eqterms

print("hello")
with open("test.json") as jsonFile:
    jsonContents = json.load(jsonFile)
    print(type(jsonContents))
    # program
    match jsonContents:
        # m_prog
        case {'types':_,'declarations':_,'functions':_}:
            # prog = m_prog()
            print("MATCHED")

        # m_decl 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")

# CONSIDER USING | (or)
        # m_type (int)
        case 'int':
            # type = m_type()
            print("MATCHED")

        # m_type (string)
        case 'string':
            # type = m_type()
            print("MATCHED")

        # m_type (struct)
        case _: # THIS ONE CANT REALLY BE RIGHT
            # type = m_type()
            print("MATCHED")



# COME BACK TO THIS
        # m_id_list 
        case {'id': ... }:
            # id_list = m_id_list()
            print("MATCHED")


# good?
        # m_declaration 
        case {'type':_,'id':_,'list':_}:
            # declaration = m_declaration()
            print("MATCHED")



# SHOULD BE JUST 1 OR MORE m_declaration. NOT SURE HOW TO DO THAT YET
        # m_declarations 
        case *{'type':_,'id':_,'list':_} : # maybe something like this??
            # declarations = m_declarations()
            print("MATCHED")




# NO CLUE HERE
        # m_nested_decl → decl ; {decl ;}∗
        case {'line':_,'type':_,'id':_}:
            # nested_decl = m_nested_decl()
            print("MATCHED")


# good?
        # m_type_declaration → struct id { nested decl } ;
        case {'line':_,'id':_,'fields':[_]}:
            # type_declaration = m_type_declaration()
            print("MATCHED")


# 0 or more m_type_declaration, still dont know how to do that
        # m_types → {type declaration}∗
        case [*{"line":_,"id":_,"fields":_}]: # this * is wrong
            # types = m_types()
            print("MATCHED")



            



        # m_parameters 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_return_type
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_return_type 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_function 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_functions 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_prog 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_assignment 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_print 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_conditional
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_loop 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_delete 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_ret 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_invocation 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")

            
        # m_statement 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED") 


        # m_statement_list 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_block 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_lvalue 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_expression
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_boolterm 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_eqterm 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_relterm 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_simple 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_term 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_unary 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_selector 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_factor 
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        # m_args
        case {'line':_,'type':_,'id':_}:
            # decl = m_decl()
            print("MATCHED")


        case _:
            print("FAILED")

class m_arguments:
    def __init__(self, expressions:list[m_expression] = None):
        self.expressions = expressions


"""
TASK 2: recursively parse json file into python classes
    should return a m_program object
    pattern match at each level of json file: https://www.python.org/dev/peps/pep-0636/
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""

print("hello")
with open("test.json") as jsonFile:
    jsonContents = json.load(jsonFile)
    match jsonContents:
        case {'types':_,'declarations':_,'functions':_}:
            # prog = m_prog()
            print("MATCHED")
        case _:
            print("FAILED")


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