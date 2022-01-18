import unittest
import json
from ast_class_definitions import *
from json_parser import parse
import test_ast_trees_andrew

class test_json_parser(unittest.TestCase):

    def test_basic(self):
        with open('json_parser_tests/basic.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees_andrew.expected1)
    
    def test_function(self):
        with open('json_parser_tests/function.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected2
        self.assertEqual(ast, test_ast_trees_andrew.expected2)
    
    def test_function_1(self):
        with open('json_parser_tests/function_1.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees_andrew.expected3)

    def test_loop(self):
        with open('json_parser_tests/loop.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees_andrew.expected4)

    def test_if(self):
        with open('json_parser_tests/if.json') as file:
            contents = json.load(file)
        ast = parse(contents)

        self.assertEqual(ast, test_ast_trees_andrew.expected5)

    def test_structs(self):
        with open('json_parser_tests/structs.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected6
        self.assertEqual(ast, expected)

    def test_functionCall(self):
        with open('json_parser_tests/functionCall.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected7

        self.assertEqual(ast, expected)

    def test_dot(self):
        with open('json_parser_tests/dot.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected8

        self.assertEqual(ast, expected)

    def test_unary(self):
        with open('json_parser_tests/unary.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected9
        self.assertEqual(ast, expected)
        # doesn't actually compare with ast but will print error message if 
        # there are any unrecognized structures in the json

    def test_mini1(self):
        with open('json_parser_tests/1.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        pass
        # doesn't actually compare with ast but will print error message if 
        # there are any unrecognized structures in the json

    def test_mini2(self):
        with open('json_parser_tests/2.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        # doesn't actually compare with ast but will print error message if 
        # there are any unrecognized structures in the json

if __name__ == '__main__':
    unittest.main()