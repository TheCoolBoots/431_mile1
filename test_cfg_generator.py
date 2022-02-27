import unittest
import json
from ast_class_definitions import *
from top_compiler import importMiniFile
from cfg_generator import generateProgCFGs

class test_cfg_generator(unittest.TestCase):

    def test_if_oneReturn(self):
        ast = importMiniFile('miniFiles/if_oneReturn.mini')
        functions = generateProgCFGs(ast)
        
        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {',
                                '  1 -> 2;',
                                '  2 -> 3;',
                                '  2 -> 4;',
                                '  3 -> 0;',
                                '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: if guard node',
                            '3: statement block node',
                            '4: if exit node',
                            '0: return node']
        self.assertEqual(labels, expectedLabels)


    def test_if_bothReturn(self):
        ast = importMiniFile('miniFiles/if_bothReturn.mini')
        functions = generateProgCFGs(ast)

        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {',
                                '  1 -> 2;',
                                '  2 -> 3;',
                                '  2 -> 4;',
                                '  3 -> 0;',
                                '  4 -> 0;',
                                '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: if guard node',
                            '3: statement block node',
                            '4: statement block node',
                            '0: return node']
        self.assertEqual(labels, expectedLabels)

    def test_if_onePass(self):
        ast = importMiniFile('miniFiles/if_onePass.mini')
        functions = generateProgCFGs(ast)
        serialized = functions[0].serialize()

        expectedSerialized = ['digraph "cfg" {',
                                '  1 -> 2;',
                                '  2 -> 3;',
                                '  2 -> 4;',
                                '  3 -> 4;',
                                '}']
        self.assertEqual(serialized, expectedSerialized)
    
        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: if guard node',
                            '3: statement block node',
                            '4: if exit node',]
        self.assertEqual(labels, expectedLabels)
        print(nodes[1].nextNodes[0].label, nodes[1].nextNodes[1].label)



    def test_if_bothPass(self):
        ast = importMiniFile('miniFiles/if_bothPass.mini')
        functions = generateProgCFGs(ast)

        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {',
                                '  1 -> 2;',
                                '  2 -> 3;',
                                '  2 -> 4;',
                                '  3 -> 5;',
                                '  4 -> 5;',
                                '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: if guard node',
                            '3: statement block node',
                            '4: statement block node',
                            '5: if exit node']
        self.assertEqual(labels, expectedLabels)

    def test_while_ret(self):
        ast = importMiniFile('miniFiles/while_ret.mini')
        functions = generateProgCFGs(ast)

        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {', 
                            '  1 -> 2;', 
                            '  2 -> 3;', 
                            '  2 -> 4;', 
                            '  3 -> 0;', 
                            '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: while guard node',
                            '3: statement block node',
                            '4: while exit node',
                            '0: return node']
        self.assertEqual(labels, expectedLabels)

    def test_while_pass(self):
        ast = importMiniFile('miniFiles/while_pass.mini')
        functions = generateProgCFGs(ast)

        serialized = functions[0].serialize()
        expectedSerialized = ['digraph "cfg" {', 
                            '  1 -> 2;', 
                            '  2 -> 3;', 
                            '  2 -> 4;', 
                            '  3 -> 2;', 
                            '}']
        self.assertEqual(serialized, expectedSerialized)

        nodes = functions[0].getAllNodes()
        labels = [f'{node.id}: {node.label}' for node in nodes]
        expectedLabels = ['1: statement block node',
                            '2: while guard node',
                            '3: statement block node',
                            '4: while exit node',]
        self.assertEqual(labels, expectedLabels)

if __name__ == '__main__':
    unittest.main()