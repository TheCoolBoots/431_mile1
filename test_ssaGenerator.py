from ast_class_definitions import *
from cfg_generator import CFG_Node
from ssaGenerator import _generateSSA
import unittest
from top_compiler import importMiniFile


class test_ssa_generator(unittest.TestCase):

    def test_basic(self):
        ast = importMiniFile('ssaFormFiles/basic.mini')
        statementList = ast.functions[0].statements

        node = CFG_Node([], [], statementList, 1)

        # %1 = i32 42
        # %2 = add i32 %1, i32 %1
        # %3 = i32 23
        # %4 = add i32 %2, i32 %3

        code, mappings = _generateSSA(node, {}, {})
        expected = ["%1 = i32 42","%2 = add i32 %1, i32 %1","%3 = i32 23","%4 = add i32 %2, i32 %3"]
        self.assertEqual(code, expected)


    # t_env structure: {str: list[m_declaration]}
    def test_legacy(self):
        ast = importMiniFile('ssaFormFiles/legacy.mini')
        statementList = ast.functions[0].statements

        node = CFG_Node([], [], statementList, 1)

        types = {'A':[m_declaration(1, m_type('int'), m_id(1, 'a'))]}

        node.mappings['varHolder'] = (f'%struct.A*', f'varHolder', 'A')

        code, mappings = _generateSSA(node, types, {})
        expected = ['%1 = i32 1',
            '%2 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0',
            'store i32 %1, i32* %2',
            '%3 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0',
            '%4 = load i32, i32* %3',
            '%5 = call i32 @printf("%d", %4)',
            '%6 = bitcast %struct.A* %varHolder to i8*',
            'call void @free(%6)']

        self.assertEqual(code, expected)
        self.assertEqual(mappings, {})

    def test_return(self):
        ast = importMiniFile('ssaFormFiles/return.mini')
        statements = ast.functions[0].statements
        node = CFG_Node([],[],statements, 1)
        functions = {'foo':(m_type('void'), [m_type('int')])}

        expected = ['%1 = i32 5',
                '%2 = call void @foo(i32 %1)',
                'ret void']

        code, mappings = _generateSSA(node, {}, functions)
        self.assertEqual(code, expected)
        # mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
        self.assertEqual({'a': ('void', 2, 'placeholder')}, mappings)

    def test_globalVariables(self):
        pass
    

if __name__ == '__main__':
    unittest.main()