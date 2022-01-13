import unittest
import json
from ast_class_definitions import *
from json_parser import parseJson

class test_json_parser(unittest.TestCase):

    def test_basic(self):
        with open('json_parser_tests/basic.json') as file:
            contents = json.load(file)
        ast = parseJson(contents)
        nested_declarations = m_declarations([m_declaration(m_type('int'), m_id('a'))])
        types = m_types([m_type_declaration(m_id('B'), nested_declarations)])
        declarations = m_declarations([m_declaration(m_type('int'), m_id('i')), m_declaration(m_type('int'), m_id('j'))])
        functions = m_functions([])
        expected = m_prog(types, declarations, functions)
        self.assertEqual(ast, expected)

if __name__ == '__main__':
    unittest.main()