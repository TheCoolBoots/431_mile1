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