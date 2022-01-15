from ast_class_definitions import *


# trivial program (True):
# int i; 
types_a = m_types([])
declarations_a = m_declarations([m_declaration(m_type('int'), m_id('i'))])
functions_a = m_functions([])
prog_a = m_prog(types_a, declarations_a, functions_a)


# # THIS ISNT LEGAL
# # trivial program (True): 
# # int i; 
# # i = 1; # NOT SURE I CAN HAVE ASSIGNMENT OUTSIDE A FUNCTION
# # UNFINISHED
# types_b = m_types([])
# declarations_b = m_declarations([m_declaration(m_type('int'), m_id('i'))])
# functions_b = m_functions([])
# prog_b = m_prog(types_b, declarations_b, functions_b)


# trivial struct program (True):
# struct A{
# int a;
# };
nested_declarations_c = m_declarations([m_declaration(m_type('int'), m_id('a'))])
types_c = m_types([m_type_declaration(m_id('A'), nested_declarations_c)]) # if you have id for type, you must have nested_declarations
declarations_c = m_declarations([])
functions_c = m_functions([])
prog_c = m_prog(types_c, declarations_c, functions_c)


# trivial struct program (True):
# struct A{
# int a;
# bool b;
# };
nested_declarations_d = m_declarations([m_declaration(m_type('int'), m_id('a')), m_declaration(m_type('bool'), m_id('b'))])
types_d = m_types([m_type_declaration(m_id('A'), nested_declarations_d)]) # if you have id for type, you must have nested_declarations
declarations_d = m_declarations([])
functions_d = m_functions([])
prog_d = m_prog(types_d, declarations_d, functions_d)



# nested struct program (True):
# struct A{
# int a;
# };
#
# struct B{
# struct A a;
# };
nested_declarations_e1 = m_declarations([m_declaration(m_type('int'), m_id('a'))])
nested_declarations_e2 = m_declarations([m_declaration(m_type('A'), m_id('B'))])
types_e = m_types([m_type_declaration(m_id('A'), nested_declarations_e1), m_type_declaration(m_id('B'), nested_declarations_e2 )]) # if you have id for type, you must have nested_declarations
declarations_e = m_declarations([])
functions_e = m_functions([])
prog_e = m_prog(types_e, declarations_e, functions_e)


# nested struct program (True):
# struct A{
# int a;
# bool b;
# };
#
# struct B{
# struct A a;
# int b;
# };
nested_declarations_f1 = m_declarations([m_declaration(m_type('int'), m_id('a')), m_declaration(m_type('bool'), m_id('b'))])
nested_declarations_f2 = m_declarations([m_declaration(m_type('A'), m_id('a')), m_declaration(m_type('int'), m_id('b'))])
types_f = m_types([m_type_declaration(m_id('A'), nested_declarations_f1), m_type_declaration(m_id('B'), nested_declarations_f2)]) # if you have id for type, you must have nested_declarations
declarations_f = m_declarations([])
functions_f = m_functions([])
prog_f = m_prog(types_f, declarations_f, functions_f)


# nested struct program (True):
# struct A{
# int a;
# };
#
# struct A myStruct;
# A.a = 1;
# UNFINISHED
nested_declarations_g = m_declarations([m_declaration(m_type('int'), m_id('a'))])
types_g = m_types([m_type_declaration(m_id('A'), nested_declarations_g)]) # if you have id for type, you must have nested_declarations
declarations_g = m_declarations([])
functions_g = m_functions([])
prog_g = m_prog(types_g, declarations_g, functions_g)



# simplest assignment (True):
# fun main(int b) int {
#     int i;
#     i = 1;
#     return 0;
# }
types_h = m_types([])
declarations_h = m_declarations([])
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass_h = m_statement(m_assignment(m_lvalue([m_id('i')]), m_num(1)))
ret_h = m_statement(m_ret(m_num(0)))
body_h = m_statement_list([ass_h, ret_h])
params_h = m_declarations([m_declaration(m_type('int'), m_id('b'))])
decls_h = m_declarations([m_declaration(m_type('int'), m_id('i'))])
expected_h = m_function(m_id('main'), params_h, m_type('int'), decls_h, body_h)
functions_h = m_functions([expected_h])
prog_h = m_prog(types_h, declarations_h, functions_h)


# derived from function.json (True):
# fun main(int b) int {
#     int i;
#     i = 2 - 3;
#     return 0;
# }
types2 = m_types([])
declarations2 = m_declarations([])
binop2 = m_binop('-', m_num(2), m_num(3))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass2 = m_statement(m_assignment(m_lvalue([m_id('i')]), binop2))
ret2 = m_statement(m_ret(m_num(0)))
body2 = m_statement_list([ass2, ret2])
params2 = m_declarations([m_declaration(m_type('int'), m_id('b'))])
decls2 = m_declarations([m_declaration(m_type('int'), m_id('i'))])
expected2 = m_function(m_id('main'), params2, m_type('int'), decls2, body2)
functions2 = m_functions([expected2])
prog2 = m_prog(types2, declarations2, functions2)