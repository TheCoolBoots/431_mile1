import unittest
import json
from ast_class_definitions import *
from json_parser import parse
import test_ast_trees_andrew

class test_json_parser(unittest.TestCase):

    # def test_basic(self):
    #     with open('json_parser_tests/basic.json') as file:
    #         contents = json.load(file)
    #     ast = parse(contents)

    #     self.assertEqual(ast, test_ast_trees_andrew.expected1)
    
    # def test_function(self):
    #     with open('json_parser_tests/function.json') as file:
    #         contents = json.load(file)
    #     ast = parse(contents)

    #     self.assertEqual(ast, test_ast_trees_andrew.expected2)
    
    # def test_function_1(self):
    #     with open('json_parser_tests/function_1.json') as file:
    #         contents = json.load(file)
    #     ast = parse(contents)

    #     self.assertEqual(ast, test_ast_trees_andrew.expected3)

    # def test_loop(self):
    #     with open('json_parser_tests/loop.json') as file:
    #         contents = json.load(file)
    #     ast = parse(contents)

    #     self.assertEqual(ast, test_ast_trees_andrew.expected4)

    # def test_if(self):
    #     with open('json_parser_tests/if.json') as file:
    #         contents = json.load(file)
    #     ast = parse(contents)

    #     self.assertEqual(ast, test_ast_trees_andrew.expected5)

    def test_structs(self):
        with open('json_parser_tests/structs.json') as file:
            contents = json.load(file)
        ast = parse(contents)
        expected = test_ast_trees_andrew.expected6
        print(ast.functions.functions[0].statement_list == expected.functions.functions[0].statement_list)
        print(ast.functions.functions[0].declarations == expected.functions.functions[0].declarations)
        self.assertEqual(ast, expected)

if __name__ == '__main__':
    unittest.main()