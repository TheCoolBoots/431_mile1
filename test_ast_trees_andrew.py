from ast_class_definitions import *


# derived from basic.json
nested_declarations1 = m_declarations([m_declaration(m_type('int'), m_id('a'))])
types1 = m_types([m_type_declaration(m_id('B'), nested_declarations1)])
declarations1 = m_declarations([m_declaration(m_type('int'), m_id('i')), m_declaration(m_type('int'), m_id('j'))])
functions1 = m_functions([])
expected1 = m_prog(types1, declarations1, functions1)


# derived from function.json
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

expected2 = m_prog(types2, declarations2, functions2)


# derived from function_1.json
types3 = m_types([])
declarations3 = m_declarations([])

inner_binop3 = m_binop('-', m_num(2), m_num(3))
outer_binop3 = m_binop('+', inner_binop3, m_num(5))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass3 = m_statement(m_assignment(m_lvalue([m_id('i')]), outer_binop3))
ret3 = m_statement(m_ret(m_num(0)))
body3 = m_statement_list([ass3, ret3])
params3 = m_declarations([m_declaration(m_type('int'), m_id('b'))])
decls3 = m_declarations([m_declaration(m_type('int'), m_id('i'))])

expectedFuns3 = m_function(m_id('main'), params3, m_type('int'), decls3, body3)
functions3 = m_functions([expectedFuns3])

expected3 = m_prog(types3, declarations3, functions3)


# derived from loop.json
whileBody4 = m_block(m_statement_list([m_statement(m_print(m_num(7), False))]))
whileGuard4 = m_bool(True)
whileStatement4 = m_statement(m_loop(whileGuard4, whileBody4))
mainBody4 = m_function(m_id('main'), m_declarations([]), m_type('int'), m_declarations([]), m_statement_list([whileStatement4])) 
functions4 = m_functions([mainBody4])
expected4 = m_prog(m_types([]), m_declarations([]), functions4)


# derived from if.json
thenBlock5 = m_block(m_statement_list([m_statement(m_print(m_num(7), False))]))
guardClause5 = m_binop('==', m_id('a'), m_num(3))
ifStatement5 = m_statement(m_conditional(guardClause5, thenBlock5))
assignStatement5 = m_statement(m_assignment(m_lvalue([m_id('a')]), m_num(3)))

functionBody5 = m_statement_list([assignStatement5, ifStatement5])
declarations5 = m_declarations([m_declaration(m_type('int'), m_id('a'))])
mainBody5 = m_function(m_id('main'), m_declarations([]), m_type('int'), declarations5, functionBody5) 

expected5 = m_prog(m_types([]), m_declarations([]), m_functions([mainBody5]))


# derived from structs.json
nestedDeclarations6 = m_declarations([m_declaration(m_type('int'), m_id('a')), m_declaration(m_type('int'), m_id('b'))])