from ast_class_definitions import *


# derived from basic.json
nested_declarations1 = [m_declaration(3, m_type('int'), m_id(3, 'a'))]
types1 = [m_type_declaration(1, m_id(1, 'B'), nested_declarations1)]
declarations1 = [m_declaration(5, m_type('int'), m_id(5, 'i')), m_declaration(5, m_type('int'), m_id(5, 'j'))]
functions1 = []
expected1 = m_prog(types1, declarations1, functions1)


# derived from function.json
binop2 = m_binop(4, '-', m_num(2), m_num(3))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass2 = m_assignment(4, [m_id(4, 'i')], binop2)
ret2 = m_ret(5, m_num(0))
body2 = [ass2, ret2]
params2 = [m_declaration(1, m_type('int'), m_id(1, 'b'))]
decls2 = [m_declaration(3, m_type('int'), m_id(3, 'i'))]
functions2 = [m_function(1, m_id(1, 'main'), params2, m_type('int'), decls2, body2)]

expected2 = m_prog([], [], functions2)


# derived from function_1.json
inner_binop3 = m_binop(4, '-', m_num(2), m_num(3))
outer_binop3 = m_binop(4, '+', inner_binop3, m_num(5))
# NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
ass3 = m_assignment(4, [m_id(4, 'i')], outer_binop3)
ret3 = m_ret(5, m_num(0))
body3 = [ass3, ret3]
params3 = [m_declaration(1, m_type('int'), m_id(1, 'b'))]
decls3 = [m_declaration(3, m_type('int'), m_id(3, 'i'))]

expectedFuns3 = m_function(1, m_id(1, 'main'), params3, m_type('int'), decls3, body3)
functions3 = [expectedFuns3]

expected3 = m_prog([], [], functions3)


# derived from loop.json
whileBody4 = [m_print(5, m_num(7), False)]
whileGuard4 = m_bool(True)
whileStatement4 = m_loop(3, whileGuard4, whileBody4)
mainBody4 = m_function(1, m_id(1, 'main'), [], m_type('int'), [], [whileStatement4])
functions4 = [mainBody4]
expected4 = m_prog([], [], functions4)


# derived from if.json
thenBlock5 = [m_print(7, m_num(7), False)]
guardClause5 = m_binop(5, '==', m_id(5,'a'), m_num(3))
ifStatement5 = m_conditional(5, guardClause5, thenBlock5)
assignStatement5 = m_assignment(4, [m_id(4, 'a')], m_num(3))

functionBody5 = [assignStatement5, ifStatement5]
declarations5 = [m_declaration(3, m_type('int'), m_id(3, 'a'))]
mainBody5 = m_function(1, m_id(1, 'main'), [], m_type('int'), declarations5, functionBody5) 

expected5 = m_prog([], [], [mainBody5])


# derived from structs.json
nestedDeclarations6 = [m_declaration(2, m_type('int'), m_id(2, 'a')), m_declaration(3, m_type('int'), m_id(3, 'b'))]
typeDeclarations6 = m_type_declaration(1, m_id(1, 'A'), nestedDeclarations6)
types6 = [typeDeclarations6]

assignmentStatement6 = m_assignment(8, [m_id(8, 'A'), m_id(8, 'a')], m_num(5))
functionDeclaration6 = m_declaration(7, m_type('A'), m_id(7, 'temp'))
function6 = m_function(6, m_id(6, 'main'), [], m_type('int'), [functionDeclaration6], [assignmentStatement6])
expected6 = m_prog(types6, [], [function6])


# derived from functionCall.json
types7 = [m_type_declaration(1, m_id(1, 'A'), [m_declaration(2, m_type('int'), m_id(2, 'a'))])]

function1_7 = m_function(5, m_id(5, 'foo'), [m_declaration(5, m_type('A'), m_id(5, 'tmp'))], m_type('int'), [], [m_ret(7, m_num(5))])
assignStatement7 = m_assignment(13, [m_id(13, 'a')], m_invocation(13, m_id(13, 'foo'), [m_new_struct(m_id(13, 'A'))]))
returnStatement7 = m_ret(14, m_num(0))
function2_7 = m_function(10, m_id(10, 'main'), [], m_type('int'), [m_declaration(12, m_type('int'), m_id(12, 'a'))], [assignStatement7, returnStatement7])
expected7 = m_prog(types7, [], [function1_7, function2_7])


# derived from dot.json
structA8 = m_type_declaration(1, m_id(1, 'A'), [m_declaration(3, m_type('int'), m_id(3, 'i')), m_declaration(4, m_type('A'), m_id(4, 'a'))])
structB8 = m_type_declaration(6, m_id(6, 'B'), [m_declaration(8, m_type('A'), m_id(8, 'a'))])
ret8 = m_ret(13, [m_id(13, 'b'), m_id(13, 'a'), m_id(13, 'a'), m_id(13, 'a'), m_id(13, 'a'), m_id(13, 'i')])
function8 = m_function(10, m_id(10, 'main'), [], m_type('int'), [m_declaration(12, m_type('B'), m_id(12, 'b'))], [ret8])
expected8 = m_prog([structA8, structB8], [], [function8])


# derived from unary.json
ret9 = m_ret(3, m_unary(3, '!', m_bool(True)))
function9 = m_function(1, m_id(1, 'main'), [], m_type('int'), [], [ret9])
expected9 = m_prog([],[],[function9])