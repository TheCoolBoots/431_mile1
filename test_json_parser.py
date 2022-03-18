import unittest
import json
from ast_class_definitions import *
from json_parser import parse
import test_ast_trees

class test_json_parser(unittest.TestCase):

    def test_mixed(self):
        with open('benchmarks/mixed/mixed.json') as file:
            contents = json.load(file)
        ast = parse(contents)

if __name__ == '__main__':
    unittest.main()