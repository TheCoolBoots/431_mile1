# import pandas as pd
# import numpy as np
import json

"""
TASK 1: create python class for each format as described in overview.pdf
    name class m_[name of thing]
    ex def m_program(types declarations functions)
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""

# program → types declarations functions
def m_prog(types:m_types, declarations, functions):
    def __init__(self, types, declarations, functions):
      self.types = types
      self.declarations = declarations
      self.functions = functions




        


# types → {type declaration}∗

# type declaration → struct id { nested decl } ;

# nested decl → decl ; {decl ;}∗

# decl → type id

# type → int | bool | struct id

# declarations → {declaration}∗

# declaration → type id list ;

# id list → id {,id}∗

# functions → {function}∗

# function → fun id parameters return type { declarations statement list }

# parameters → ( {decl {,decl}∗}opt)

# return type → type | void

# statement → block | assignment | print | conditional | loop | delete | ret | invocation

# block → { statement list }

# statement list → {statement}∗

# assignment → lvalue = { expression | read } ;

# print → print expression {endl}opt;

# conditional → if ( expression ) block {else block}opt

# loop → while ( expression ) block

# delete → delete expression ;

# ret → return {expression}opt;

# invocation → id arguments ;



# lvalue → id {.id}∗
def m_lvalue(m_ids:list[m_id]):
    def __init__(self, m_ids):
        self.m_ids = m_ids


# expression → boolterm {|| boolterm}∗
def m_expression(boolterms:list[m_boolterm], operators:list[str] ):
    def __init__(self, boolterms, operators):
        self.boolterms = boolterms
        self.operators = operators


# boolterm → eqterm {&& eqterm}∗
def m_boolterm(eqterms:list[eqterm], operators:list[str] ):
    def __init__(self, eqterms, operators):
        self.eqterms = eqterms
        self.operators = operators


# SIMLAR TO RELTERM, SIMPLE, TERM, AND UNARY, NOT SURE WHAT TO DO WITH THE OPERATORS
# eqterm → relterm {{== | ! =} relterm}∗
def m_eqterm(relterms:list[m_relterm], operators:list[str]):
    def __init__(self, relterms, operators):
        self.relterms = relterms
        self.operators = operators


# SIMLAR TO SIMPLE, TERM, AND UNARY, NOT SURE WHAT TO DO WITH THE OPERATORS
# relterm → simple {{<| >| <= | >=} simple}∗
def m_relterm(simples:list[m_simple], operators:list[str]):
    def __init__(self, simples, operators):
        self.simples = simples
        self.operators = operators


# SIMLAR TO TERM AND UNARY, NOT SURE WHAT TO DO HERE
# simple → term {{+ | −} term}∗
def m_simple(terms:list[m_term], operators:list[str] ):
    def __init__(self, terms:list[m_term], operators:list[str]):
        self.terms = terms
        self.operators = operators


# NOT SURE HOW TO DEAL WITH * AND / HERE
# term → unary {{∗ | /} unary}∗
def m_term(unarys:list[m_unary], operators:list[str]):
    def __init__(self, unarys:list[m_unary], operators:list[str]):
        self.unarys = unarys
        self.operators = operators


# WASNT SURE WHAT TO PUT IN THE operator FIELD FOR - AND !
# unary → {! | −}∗selector
def m_unary(operators:list[str], selector:m_selector):
    def __init__(self, operators:list[str], selector[m_selector]):
        self.operators = operators
        self.selector = selector


# NOT SURE WHAT THE . BEFORE id indicates here
# selector → factor {.id}∗
def m_selector(factor:m_factor, identifiers:list[m_id]):
    def __init__(self, factor:m_factor, identifiers:list[m_id]):
        self.factor = factor
        self.identifiers = identifiers


# THIS IS WEIRD WITH MULTIPLE FIELDS IN SOME PLACES
# THERE IS AN UNDERLINE UNDER THE expression PARENS, WHAT DOES THIS MEAN?
# factor → ( expression ) | id {arguments}opt| number | true | false | new id | null
def m_factor(factorInput):
    def __init__(expression:m_expression):
      self.expression = expression

    # def __init__(:):
    #   self. = 
    # def __init__(expression:m_expression):
    #   self.expression = expression
    # def __init__(expression:m_expression):
    #   self.expression = expression
      

# THERE IS AN UNDERLINE UNDER THE OUTSIDE PARENS, WHAT DOES THIS MEAN?
# arguments → ( {expression {,expression}∗}opt)
def m_args(expressions:list[m_expression]):
    def __init__(self, expressions:list[m_expression]):
      self.expressions = expressions



print("hello")
with open("test.json") as jsonFile:
    jsonContents = json.load(jsonFile)
    print(type(jsonContents))
    match jsonContents:
        case {'types':_,'declarations':_,'functions':_}:
            # prog = m_prog()
            print("MATCHED")
        case _:
            print("FAILED")



"""
TASK 2: recursively parse json file into python classes
    should return a m_program object
    pattern match at each level of json file: https://www.python.org/dev/peps/pep-0636/
    NOTE maybe this isn't required? can do all semantic checks just on json?
"""


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