from ast_class_definitions import *


# derived from basic.json
nested_declarations1 = [m_declaration(m_type('int'), m_id('a'))]
types1 = [m_type_declaration(m_id('B'), nested_declarations1)]
declarations1 = [m_declaration(m_type('int'), m_id('i')), m_declaration(m_type('int'), m_id('j'))]
functions1 = []
expected1 = m_prog(types1, declarations1, functions1)


# derived from function.json
binop2 = m_binop('-', m_num(2), m_num(3))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass2 = m_assignment([m_id('i')], binop2)
ret2 = m_ret(m_num(0))
body2 = [ass2, ret2]
params2 = [m_declaration(m_type('int'), m_id('b'))]
decls2 = [m_declaration(m_type('int'), m_id('i'))]
functions2 = [m_function(m_id('main'), params2, m_type('int'), decls2, body2)]

expected2 = m_prog([], [], functions2)


# derived from function_1.json
inner_binop3 = m_binop('-', m_num(2), m_num(3))
outer_binop3 = m_binop('+', inner_binop3, m_num(5))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass3 = m_assignment([m_id('i')], outer_binop3)
ret3 = m_ret(m_num(0))
body3 = [ass3, ret3]
params3 = [m_declaration(m_type('int'), m_id('b'))]
decls3 = [m_declaration(m_type('int'), m_id('i'))]

expectedFuns3 = m_function(m_id('main'), params3, m_type('int'), decls3, body3)
functions3 = [expectedFuns3]

expected3 = m_prog([], [], functions3)


# derived from loop.json
whileBody4 = [m_print(m_num(7), False)]
whileGuard4 = m_bool(True)
whileStatement4 = m_loop(whileGuard4, whileBody4)
mainBody4 = m_function(m_id('main'), [], m_type('int'), [], [whileStatement4])
functions4 = [mainBody4]
expected4 = m_prog([], [], functions4)


# derived from if.json
thenBlock5 = [m_print(m_num(7), False)]
guardClause5 = m_binop('==', m_id('a'), m_num(3))
ifStatement5 = m_conditional(guardClause5, thenBlock5)
assignStatement5 = m_assignment([m_id('a')], m_num(3))

functionBody5 = [assignStatement5, ifStatement5]
declarations5 = [m_declaration(m_type('int'), m_id('a'))]
mainBody5 = m_function(m_id('main'), [], m_type('int'), declarations5, functionBody5) 

expected5 = m_prog([], [], [mainBody5])


# derived from structs.json
nestedDeclarations6 = [m_declaration(m_type('int'), m_id('a')), m_declaration(m_type('int'), m_id('b'))]
typeDeclarations6 = m_type_declaration(m_id('A'), nestedDeclarations6)
types6 = [typeDeclarations6]

assignmentStatement6 = m_assignment([m_id('A'), m_id('a')], m_num(5))
functionDeclaration6 = m_declaration(m_type('A'), m_id('temp'))
function6 = m_function(m_id('main'), [], m_type('int'), [functionDeclaration6], [assignmentStatement6])
expected6 = m_prog(types6, [], [function6])


# derived from functionCall.json
types7 = [m_type_declaration(m_id('A'), [m_declaration(m_type('int'), m_id('a'))])]
function1_7 = m_function(m_id('foo'), [m_declaration(m_type('A'), m_id('int'))], m_type('int'), [], [m_ret(m_num(5))])
function2_7 = m_function(m_id('main'), [], [m_declaration(m_type('int'), m_id('a'))], [m_declaration(m_type('int'), m_id('a'))], [])