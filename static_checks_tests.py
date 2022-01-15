import unittest
import json
from ast_class_definitions import *
from json_parser import parse

class test_type_checker(unittest.TestCase):

    # simple test case, just one declaration globally
    def test_0(self):
        nested_declarations = m_declarations([m_declaration(m_type('int'), m_id('a'))])
        types = m_types([])
        declarations = m_declarations([m_declaration(m_type('int'), m_id('i'))])
        functions = m_functions([])
        expected = m_prog(types, declarations, functions)

        # struct B {
        #   int a;
        # };
        # 
        # int i;
        # int j;

        self.assertEqual( True, type_check(expected, {}, {}) )




    def test_1(self):
        nested_declarations = m_declarations([m_declaration(m_type('int'), m_id('a'))])
        types = m_types([m_type_declaration(m_id('B'), nested_declarations)])
        declarations = m_declarations([m_declaration(m_type('int'), m_id('i')), m_declaration(m_type('int'), m_id('j'))])
        functions = m_functions([])
        expected = m_prog(types, declarations, functions)

        # struct B {
        #   int a;
        # };
        # 
        # int i;
        # int j;

        self.assertEqual( True, type_check(expected, {}, {}) )


    def test2(self):