import unittest
import json
from ast_class_definitions import *
from json_parser import parse

class test_json_parser(unittest.TestCase):

    def test_basic(self):
        with open('json_parser_tests/basic.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        nested_declarations = m_declarations([m_declaration(m_type('int'), m_id('a'))])
        types = m_types([m_type_declaration(m_id('B'), nested_declarations)])
        declarations = m_declarations([m_declaration(m_type('int'), m_id('i')), m_declaration(m_type('int'), m_id('j'))])
        functions = m_functions([])
        expected = m_prog(types, declarations, functions)
        self.assertEqual(ast, expected)
    
    def test_function(self):
        with open('json_parser_tests/function.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        types = m_types([])
        declarations = m_declarations([])

        binop = m_binop('-', m_num(2), m_num(3))
        # NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
        ass = m_statement(m_assignment(m_lvalue([m_id('i')]), binop))
        ret = m_statement(m_ret(m_num(0)))
        body = m_statement_list([ass, ret])
        params = m_declarations([m_declaration(m_type('int'), m_id('b'))])
        decls = m_declarations([m_declaration(m_type('int'), m_id('i'))])

        expected = m_function(m_id('main'), params, m_type('int'), decls, body)
        functions = m_functions([expected])

        expectedProg = m_prog(types, declarations, functions)

        self.assertEqual(ast, expectedProg)
    
    def test_function_1(self):
        with open('json_parser_tests/function_1.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        types = m_types([])
        declarations = m_declarations([])

        inner_binop = m_binop('-', m_num(2), m_num(3))
        outer_binop = m_binop('+', inner_binop, m_num(5))
        # NOTE may be able to replace m_lvalue with just m_id; look into that later -AL 1/13/21 5:26pm
        ass = m_statement(m_assignment(m_lvalue([m_id('i')]), outer_binop))
        ret = m_statement(m_ret(m_num(0)))
        body = m_statement_list([ass, ret])
        params = m_declarations([m_declaration(m_type('int'), m_id('b'))])
        decls = m_declarations([m_declaration(m_type('int'), m_id('i'))])

        expected = m_function(m_id('main'), params, m_type('int'), decls, body)
        functions = m_functions([expected])

        expectedProg = m_prog(types, declarations, functions)

        self.assertEqual(ast, expectedProg)

    def test_loop(self):
        with open('json_parser_tests/loop.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        whileBody = m_block(m_statement_list([m_statement(m_print(m_num(7), False))]))
        whileGuard = m_bool(True)
        whileStatement = m_statement(m_loop(whileGuard, whileBody))
        mainBody = m_function(m_id('main'), m_declarations([]), m_type('int'), m_declarations([]), m_statement_list([whileStatement])) 
        functions = m_functions([mainBody])
        expectedProg = m_prog(m_types([]), m_declarations([]), functions)

        self.assertEqual(ast, expectedProg)

    def test_if(self):
        with open('json_parser_tests/if.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        thenBlock = m_block(m_statement_list([m_statement(m_print(m_num(7), False))]))
        guardClause = m_binop('==', m_id('a'), m_num(3))
        ifStatement = m_statement(m_conditional(guardClause, thenBlock))
        assignStatement = m_statement(m_assignment(m_lvalue([m_id('a')]), m_num(3)))

        functionBody = m_statement_list([assignStatement, ifStatement])
        declarations = m_declarations([m_declaration(m_type('int'), m_id('a'))])
        mainBody = m_function(m_id('main'), m_declarations([]), m_type('int'), declarations, functionBody) 
        
        expectedProg = m_prog(m_types([]), m_declarations([]), m_functions([mainBody]))

        self.assertEqual(ast, expectedProg)

if __name__ == '__main__':
    unittest.main()