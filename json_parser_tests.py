import unittest
import json
from ast_class_definitions import *
from json_parser import parse
import test_ast_trees

class test_json_parser(unittest.TestCase):

    def test_basic(self):
        with open('json_parser_tests/basic.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, )
    
    def test_function(self):
        with open('json_parser_tests/function.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees.expected2)
    
    def test_function_1(self):
        with open('json_parser_tests/function_1.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees.expected3)

    def test_loop(self):
        with open('json_parser_tests/loop.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees.expected4)

    def test_if(self):
        with open('json_parser_tests/if.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees.expected5)

if __name__ == '__main__':
    unittest.main()