import unittest
from ast_class_definitions import *
from type_checker import *
import test_ast_trees

top_env = {'a': (3, m_type('int'))}
type_env = {'BIGCHUNGUS':{'a': (1, m_type('bool'))}, 'int':m_type('int'), 'bool':m_type('bool')}
local_env = {'b': (4, m_type('BIGCHUNGUS'))}

# {str : (int, m_type)}                     map id to type

# {str : {str : (int, m_type)}}             map struct id to struct contents

# {str : (int, m_type, list[m_type])}       map function id to (lineNum, retType, argTypes)

class test_type_checker(unittest.TestCase):

    def test_delete(self):
        delete = m_delete(5, m_bool(True))
        self.assertEqual(-1, typeCheck(delete, local_env, top_env, type_env, {}))

        delete = m_delete(5, m_id(5, 'b'))
        self.assertEqual(None, typeCheck(delete, local_env, top_env, type_env, {}))

    def test_dot(self):
        dot = m_dot(6, [m_id(5, 'b'), m_id(5, 'a')])
        actual = typeCheck(dot, local_env, top_env, type_env, {})
        self.assertEqual(m_type('bool'), actual)

        dot = m_dot(6, [m_id(5, 'a')])
        actual = typeCheck(dot, local_env, top_env, type_env, {})
        self.assertEqual(m_type('int'), actual)

        # 324 - struct id doesnt exist
        dot = m_dot(6, [m_id(5, 'd'), m_id(5, 'c')])
        actual = typeCheck(dot, local_env, top_env, type_env, {})
        self.assertEqual(-1, actual)

        # 335 - nested id doesnt exist
        dot = m_dot(6, [m_id(5, 'b'), m_id(5, 'c')])
        actual = typeCheck(dot, local_env, top_env, type_env, {})
        self.assertEqual(-1, actual)

    def test_invocation(self):
        functionEnv = {'foo':(3, m_type('BIGCHUNGUS'), [m_type('int')])}
        functionInvocation = m_invocation(5, m_id(5, 'foo'), [m_num(5)])
        actual = typeCheck(functionInvocation, local_env, top_env, type_env, functionEnv)
        self.assertEqual(m_type('BIGCHUNGUS'), actual)
        
        # 271
        functionEnv = {'foo':(3, m_type('BIGCHUNGUS'), [m_type('int')])}
        functionInvocation = m_invocation(5, m_id(5, 'foo'), [m_num(5),  m_num(6)])
        actual = typeCheck(functionInvocation, local_env, top_env, type_env, functionEnv)
        self.assertEqual(-1, actual)
        functionEnv = {'foo':(3, m_type('BIGCHUNGUS'), [m_type('int')])}
        functionInvocation = m_invocation(5, m_id(5, 'foo'), [])
        actual = typeCheck(functionInvocation, local_env, top_env, type_env, functionEnv)
        self.assertEqual(-1, actual)

    def test_basic(self):
        self.assertEqual(m_type('bool'), typeCheck(m_bool(True), {}, top_env, {}, {}))
        self.assertEqual(m_type('int'), typeCheck(m_num(5), {}, top_env, {}, {}))
        self.assertEqual(m_type('null'), typeCheck(m_null(), {}, top_env, {}, {}))

    def test_m_id(self):
        self.assertEqual(m_type('BIGCHUNGUS'), typeCheck(m_id(5, 'b'), local_env, top_env, type_env, {}))
        self.assertEqual(m_type('int'), typeCheck(m_id(5, 'a'), local_env, top_env, type_env, {}))

        self.assertEqual(-1, typeCheck(m_id(5, 'z'), local_env, top_env, type_env, {}))

    def test_assignment(self):
        assign = m_assignment(5, [m_id(5, 'b'), m_id(5, 'a')], m_bool(True))
        self.assertEqual(typeCheck(assign, local_env, top_env, type_env, {}), None)

        # 114 - assigns value to a variable that is declared later 
        # a1 = 10;
        # int a1;
        assign = m_assignment(1, [m_id(1, 'a1')], 10)
        currLocalEnv = {'a1' : (2, m_type('int'))}
        self.assertEqual(typeCheck(assign, currLocalEnv, {}, {}, {}), -1)

        # 125 - assigns value to a variable (not first) that is declared later 
        # int b1;
        # b1, a1 = 10;
        # int a1;
        assign = m_assignment(1, [m_id(2, 'b1'), m_id(2, 'a1')], 10)
        currLocalEnv = {'b1' : (1, m_type('int')), 'a1' : (3, m_type('int'))}
        self.assertEqual(typeCheck(assign, currLocalEnv, {}, {}, {}), -1)

        # 130 assigns value to a variable that is the wrong type
        # bool a1;
        # a1 = 10;
        assign = m_assignment(2, [m_id(2, 'a1')], 10)
        currLocalEnv = {'a1' : (1, m_type('bool'))}
        self.assertEqual(typeCheck(assign, currLocalEnv, top_env, type_env, {}), -1)

    def test_print(self):
        printStatement = m_print(5, m_num(7), False)
        self.assertEqual(typeCheck(printStatement, local_env, top_env, type_env, {}), None)
        
        # 144 - try to print things that arent ints
        printStatement = m_print(5, m_bool(False), False)
        self.assertEqual(typeCheck(printStatement, local_env, top_env, type_env, {}), -1)
        printStatement = m_print(5, m_id(5, 'int jk'), False)
        self.assertEqual(typeCheck(printStatement, local_env, top_env, type_env, {}), -1)

    # also handles m_ret base case
    def test_cond(self):
        self.assertEqual(None, typeCheck(test_ast_trees.ifStatement5, local_env, top_env, type_env, {}))
        self.assertEqual(None, typeCheck(test_ast_trees.ifStatementElse, local_env, top_env, type_env, {}))
        self.assertEqual(m_type('bool'), typeCheck(test_ast_trees.ifStatementElse2, local_env, top_env, type_env, {}))

        # 158 - condition is an int
        # if( 1 ) {
        #   print(7)
        # }
        currIfStatement = m_conditional(1,  m_num(1), [m_print(1, m_num(7), False)])
        self.assertEqual(-1, typeCheck(currIfStatement, local_env, top_env, type_env, {}))
        
        # 186 - branches have different return types
        # if(True) {
        #   return True
        # }
        # else {
        #   return 1
        # }
        currIfStatement = m_conditional(1,  m_bool(True), [m_ret(2, m_bool(True))], [m_ret(5, m_num(1))] )
        self.assertEqual(-1, typeCheck(currIfStatement, local_env, top_env, type_env, {}))
   
    def test_loop(self):
        self.assertEqual(None, typeCheck(test_ast_trees.whileStatement4, local_env, top_env, type_env, {}))
        self.assertEqual(m_type('bool'), typeCheck(test_ast_trees.fancyLoop, local_env, top_env, type_env, {}))

        # 198 - while condition is an int
        # while (1) {
        # print(7)
        # }
        currWhileStatement = m_loop(1, m_num(1), [m_print(5, m_num(7), False)])
        self.assertEqual(-1, typeCheck(currWhileStatement, local_env, top_env, type_env, {}))

    def test_returnVoid(self):
        self.assertEqual(m_type('void'), typeCheck(m_ret(9), local_env, top_env, type_env, {}))

    def test_binop(self):
        binop = m_binop(6, '==', m_bool(True), m_num(5))
        self.assertEqual(m_type('bool'), typeCheck(binop, local_env, top_env, type_env, {}))
        binop = m_binop(6, '!=', m_bool(True), m_num(5))
        self.assertEqual(m_type('bool'), typeCheck(binop, local_env, top_env, type_env, {}))
        binop = m_binop(6, '<=', m_num(3), m_num(5))
        self.assertEqual(m_type('bool'), typeCheck(binop, local_env, top_env, type_env, {}))
        binop = m_binop(6, '+', m_num(3), m_num(5))
        self.assertEqual(m_type('int'), typeCheck(binop, local_env, top_env, type_env, {}))
        binop = m_binop(6, '&&', m_bool(3), m_bool(5))
        self.assertEqual(m_type('bool'), typeCheck(binop, local_env, top_env, type_env, {}))

        # 255 - operator is smiley
        # 3 :-) 5
        binop = m_binop(1, ':-)', m_bool(3), m_bool(5))
        self.assertEqual(-1, typeCheck(binop, local_env, top_env, type_env, {}))

    # not 100% sure on this one
    def test_struct(self):
        # 282 - reference a fake struct id
        # referencing a struct that doesnt exist
        currStruct = m_new_struct(m_id(20, 'fakeStructName'))
        self.assertEqual(-1, typeCheck(currStruct, local_env, top_env, type_env, {}))

        currStruct = m_new_struct(m_id(20, 'BIGCHUNGUS'))
        self.assertEqual(m_type('BIGCHUNGUS'), typeCheck(currStruct, local_env, top_env, type_env, {}))



    def test_unary(self):
        # 298 - not on an int
        # !5
        currUnary = m_unary(1, '!', m_num(5))
        self.assertEqual(-1, typeCheck(currUnary, local_env, top_env, type_env, {}))

        # 304 - negate True (this actual does kinda make sense tbh)
        # -True
        currUnary = m_unary(1, '-', m_bool(True))
        self.assertEqual(-1, typeCheck(currUnary, local_env, top_env, type_env, {}))

        currUnary = m_unary(1, '!', m_bool(True))
        self.assertEqual(m_type('bool'), typeCheck(currUnary, local_env, top_env, type_env, {}))

        currUnary = m_unary(1, '-', m_num(5))
        self.assertEqual(m_type('int'), typeCheck(currUnary, local_env, top_env, type_env, {}))

        # 307 - smiley on int
        # :-)100
        currUnary = m_unary(1, ':-)', m_num(100))
        self.assertEqual(-1, typeCheck(currUnary, local_env, top_env, type_env, {}))

    def test_multipleReturnTypes(self):
        ifStatement = m_conditional(3, m_bool(True), [m_ret(4, m_bool(True))])
        functionBody = [ifStatement, m_ret(5, m_num(3))]
        self.assertEqual(-1, typeCheck(m_loop(2, m_bool(True), functionBody), local_env, top_env, type_env, {}))

if __name__ == '__main__':
    unittest.main()