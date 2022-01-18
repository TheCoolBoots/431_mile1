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

    def test_basic(self):
        self.assertEqual(m_type('bool'), typeCheck(m_bool(True), {}, top_env, {}, {}))
        self.assertEqual(m_type('int'), typeCheck(m_num(5), {}, top_env, {}, {}))
        self.assertEqual(m_type('null'), typeCheck(m_null(), {}, top_env, {}, {}))

    def test_m_id(self):
        self.assertEqual(m_type('BIGCHUNGUS'), typeCheck(m_id(5, 'b'), local_env, top_env, type_env, {}))
        self.assertEqual(m_type('int'), typeCheck(m_id(5, 'a'), local_env, top_env, type_env, {}))

    def test_assignment(self):
        assign = m_assignment(5, [m_id(5, 'b'), m_id(5, 'a')], m_bool(True))
        self.assertEqual(typeCheck(assign, local_env, top_env, type_env, {}), m_type('void'))

if __name__ == '__main__':
    unittest.main()