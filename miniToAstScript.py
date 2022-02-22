
import os
import sys

import unittest
from ast_class_definitions import *
from cfg_generator import *
from json_parser import *
import test_ast_trees
import json




def main():
    
    cmdLineArgs = sys.argv
    numArgs = len(cmdLineArgs)

    if numArgs != 2:
        print("Scripts expects 2 arguments: ______ and ______")


    jarCommand = "java -jar MiniCompiler.jar " + cmdLineArgs[0] + " > " + cmdLineArgs[1]

    os.command(jarCommand)


    # STOPPED HERE, REALIZED THERES AN ISSUE WITH STORING THE AST
    

    with open('json_parser_tests/loop_if.json') as file2:
        contents = json.load(file2)
    ast = parse(contents)
    # THIS SHOULDNT BE ELSE, IT SEEMS THAT THE ELSE STATEMENTS ARENT BEING PARSED
    # dont consider the else case on line 77 of json_parse.py
    print("\n\n\n\n" + str(ast.functions[0].statements[1].else_statements) + "\n\n\n\n")
    testCFG = generate_CFG_Prog_Handler(ast)
    # printCFG(testCFG.firstNode)


