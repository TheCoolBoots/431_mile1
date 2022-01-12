# import pandas as pd
# import numpy as np
import json

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
        self.type = type
    def __init__(self, typeID:m_id):
        self.type = type

# decl → type id
class m_decl:
    def __init__(self, type, id):
      self.type = type
      self.id = id

# id list → id {,id}∗
class m_id_list:
    def __init__(self, id_list:list[m_id]):
        self.id_list = id_list

# declaration → type id list ;
class m_declaration:
    def __init__(self, type, id_list):
        self.type = type
        self.id_list = id_list

# declarations → {declaration}∗
class m_declarations:
    def __init__(self, declarations:list[m_declaration]):
      self.declarations = declarations

# nested decl → decl ; {decl ;}∗
class m_nested_decl:
    def __init__(self, declarations:list[m_decl]):
      self.declarations = declarations

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
    def __init__(self, decls:list[m_decl]):
        self.decls = decls

# return type → type | void
class m_return_type:
    def __init__(self, type:m_type):
        self.type = type
    def __init__(self, type:str):
        self.type = type    # this is for when return type is void

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
    def __init__(self, types:m_types, declarations, functions):
        self.types = types
        self.declarations = declarations
        self.functions = functions

# assignment → lvalue = { expression | read } ;
class m_assignment:
    def __init__(self, lvalue, assignmentVal):
      self.lvalue = lvalue
      self.assignmentVal = assignmentVal

# print → print expression {endl}opt;
class m_print:
    def __init__(self, expression, endl:bool):
        self.expression = expression
        self.endl = endl

# conditional → if ( expression ) block {else block}opt
class m_conditional:
    def __init__(self, expression, ifBlock, elseBlock = None):
        self.expression = expression
        self.ifBlock = ifBlock
        self.elseBlock = elseBlock

# loop → while ( expression ) block
class m_loop:
    def __init__(self, expression, block):
        self.expression = expression
        self.block = block

# delete → delete expression ;
class m_delete:
    def __init__(self, expression):
      self.expression = expression

# ret → return {expression}opt;
class m_ret:
    def __init__(self, expression = None):
        self.expression = expression

# invocation → id arguments ;
class m_invocation:
    def __init__(self, id:m_id, arguments):
        self.id = id
        self.arguments = arguments

# statement → block | assignment | print | conditional | loop | delete | ret | invocation
class m_statement:
    def __init__(self, contents): # :m_block    NOTE cyclical definition statement -> block -> statement list -> statement
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

# expression → boolterm {|| boolterm}∗

# boolterm → eqterm {&& eqterm}∗

# eqterm → relterm {{== | ! =} relterm}∗

# relterm → simple {{<| >| <= | >=} simple}∗

# simple → term {{+ | −} term}∗

# term → unary {{∗ | /} unary}∗

# unary → {! | −}∗selector

# selector → factor {.id}∗

# factor → ( expression ) | id {arguments}opt| number | true | false | new id | null

# arguments → ( {expression {,expression}∗}opt)


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