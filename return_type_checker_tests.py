from threading import local
import unittest
import json
from ast_class_definitions import *
from return_type_checker import *
import test_ast_trees_andrew

top_env = {'a': (3, m_type('int'))}
type_env = {'BIGCHUNGUS':{'a': m_type('bool')}, 'int':m_type('int'), 'bool':m_type('bool')}
local_env = {'b': (4, m_type('BIGCHUNGUS'))}

# {str : (int, m_type)}                     map id to type

# {str : {str : (int, m_type)}}             map struct id to struct contents

# {str : (int, m_type, list[m_type])}       map function id to (lineNum, retType, argTypes)

class test_json_parser(unittest.TestCase):

    def test_dot(self):
        dot = m_dot(6, [m_id(5, 'b'), m_id(5, 'a')])
        actual = typeCheck(dot, local_env, top_env, type_env, {})
        self.assertEqual(m_type('bool'), actual)

    def test_invocation(self):
        functionEnv = {'foo':(3, m_type('BIGCHUNGUS'), [m_type('int')])}
        functionInvocation = m_invocation(5, m_id(5, 'foo'), [m_num(5)])
        actual = typeCheck(functionInvocation, local_env, top_env, type_env, functionEnv)
        self.assertEqual(m_type('BIGCHUNGUS'), actual)

    def test_basic(self):
        self.assertEqual(m_type('bool'), typeCheck(m_bool(True), {}, top_env, {}, {}))
        self.assertEqual(m_type('int'), typeCheck(m_num(5), {}, top_env, {}, {}))
        self.assertEqual(m_type('null'), typeCheck(m_null(), {}, top_env, {}, {}))

    def test_m_id(self):
        self.assertEqual(m_type('BIGCHUNGUS'), typeCheck(m_id(5, 'b'), local_env, top_env, type_env, {}))
        self.assertEqual(m_type('int'), typeCheck(m_id(5, 'a'), local_env, top_env, type_env, {}))

        self.assertEqual(None, typeCheck(m_id(5, 'z'), local_env, top_env, type_env, {}))

    def test_assignment(self):
        assign = m_assignment(5, [m_id(5, 'b'), m_id(5, 'a')], m_bool(True))
        self.assertEqual(typeCheck(assign, local_env, top_env, type_env, {}), m_type('void'))

    def test_print(self):
        printStatement = m_print(5, m_num(7), False)
        self.assertEqual(typeCheck(printStatement, local_env, top_env, type_env, {}), m_type('void'))

    # also handles m_ret base case
    def test_cond(self):
        self.assertEqual(m_type('void'), typeCheck(test_ast_trees_andrew.ifStatement5, local_env, top_env, type_env, {}))
        self.assertEqual(m_type('void'), typeCheck(test_ast_trees_andrew.ifStatementElse, local_env, top_env, type_env, {}))
        self.assertEqual(m_type('bool'), typeCheck(test_ast_trees_andrew.ifStatementElse2, local_env, top_env, type_env, {}))

    def test_loop(self):
        self.assertEqual(m_type('void'), typeCheck(test_ast_trees_andrew.whileStatement4, local_env, top_env, type_env, {}))
        self.assertEqual(m_type('bool'), typeCheck(test_ast_trees_andrew.fancyLoop, local_env, top_env, type_env, {}))

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


if __name__ == '__main__':
    unittest.main()