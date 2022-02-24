from xml.etree.ElementInclude import include
from ast_class_definitions import *
from cfg_generator import CFG_Node
from ssaGenerator import generateSSA
import unittest
from top_compiler import importMiniFile


class test_ssa_generator(unittest.TestCase):

    def test_basic(self):
        ast = importMiniFile('ssaFormFiles/basic.mini')
        statementList = ast.functions[0].statements

        node = CFG_Node(0, [], [], statementList, 1)

        # %1 = i32 42
        # %2 = add i32 %1, i32 %1
        # %3 = i32 23
        # %4 = add i32 %2, i32 %3

        lastRegUsed, code = generateSSA(node, {}, {}, {})
        expected = ["%1 = i32 42","%2 = add i32 %1, i32 %1","%3 = i32 23","%4 = add i32 %2, i32 %3"]
        self.assertEqual(code, expected)


    # t_env structure: {str: list[m_declaration]}
    def test_legacy(self):
        ast = importMiniFile('ssaFormFiles/legacy.mini')
        statementList = ast.functions[0].statements

        node = CFG_Node(0, [], [], statementList, 1)

        types = {'A':[m_declaration(1, m_type('int'), m_id(1, 'a'))]}

        env = {'varHolder': (False, m_type('A'))}

        lastRegUsed, code = generateSSA(node, env, types, {})
        expected = ['%1 = i32 1', 
        '%2 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0', 
        'store i32 %1, i32* %2', 
        '%3 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0', 
        '%4 = load i32, i32* %3', 
        '%5 = call i32 @printf("%d", %4)', 
        '%6 = load %struct.A** %varHolder', 
        '%7 = bitcast %struct.A* %6 to i8*', 
        'call void @free(%7)']

        self.assertEqual(code, expected)

    def test_return(self):
        ast = importMiniFile('ssaFormFiles/return.mini')
        statements = ast.functions[0].statements
        node = CFG_Node(0, [],[],statements, 1)
        functions = {'foo':(m_type('void'), [m_type('int')])}

        expected = ['%1 = i32 5',
                '%2 = call void @foo(i32 %1)',
                'ret void']

        lastRegUsed, code = generateSSA(node, {}, {}, functions)
        self.assertEqual(code, expected)
        # mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}
        self.assertEqual({'a': ('void', 2, 'placeholder')}, node.mappings)

    def test_globals(self):
        ast = importMiniFile('ssaFormFiles/globals.mini')
        statements = ast.functions[0].statements
        node = CFG_Node(0, [],[], statements, 1)
        top_env = ast.getTopEnv(includeLineNum=False)
        types = ast.getTypes()

        expected = ['%1 = i32 5', 
                    'store i32 %1, i32* @a', 
                    '%2 = i32 4', 
                    'store i32 %2, i32* @b', 
                    '%3 = load i32* @a', 
                    '%4 = load i32* @b', 
                    '%5 = add i32 %3, i32 %4', 
                    'ret i32 %5']

        lastRegUsed, code = generateSSA(node, top_env, types, {})

        self.assertEqual(expected,code)
        self.assertEqual(node.mappings, {})

    def test_structs(self):
        ast = importMiniFile('ssaFormFiles/structs.mini')
        statements = ast.functions[0].statements
        localDeclarations = ast.functions[0].body_declarations
        top_env = ast.getTopEnv()
        types = ast.getTypes()

        node = CFG_Node(0, [],[],statements, 1)

        for localDec in localDeclarations:
            top_env[localDec.id.identifier] = (False, localDec.type)

        lastRegUsed, code = generateSSA(node, top_env, types, {})

        expected =['%1 = call i8* @malloc(8)', 
                '%1 = bitcast i8* %1 to %struct.A*', 
                'store %struct.A* %1, %struct.A** %redacted', 
                '%2 = call i8* @malloc(8)', 
                '%2 = bitcast i8* %2 to %struct.A*',
                'store %struct.A* %2, %struct.A** @beoch', 
                '%3 = getelementptr %struct.A, %struct.A* @beoch, i32 0, i32 0', 
                '%4 = load i32, i32* %3', 
                'ret i32 %4']

        self.assertEqual(code, expected)

        declarationCode = []
        for globalDec in ast.global_declarations:
            declarationCode.append(globalDec.getSSAGlobals())
        
        for localDec in localDeclarations:
            declarationCode.append(localDec.getSSALocals())

        expectedDecls = ['@beoch = common dso_local global %struct.A* null', '%redacted = alloca %struct.A*']
        self.assertEqual(declarationCode, expectedDecls)

    def test_basicPhi(self):
        currentNode = CFG_Node(0, [], [], [m_ret(0, m_id(1, 'a'))],2)

        leftNode = CFG_Node(0, [], [], [], 1)
        rightNode = CFG_Node(0, [], [], [], 1)
        leftNode.mappings['a'] = ('i32', 4, 'int')
        rightNode.mappings['a'] = ('i32', 5, 'int')

        currentNode.previousBlocks=[leftNode, rightNode]
        currentNode.sealed = True

        lastRegUsed, code = generateSSA(currentNode, {}, {}, {})
        self.assertEqual(currentNode.mappings, {'a': ('i32', 1)})
        self.assertEqual(code, ['%1 = phi(i32 %4, i32 %5)', 'ret i32 %1'])
        

if __name__ == '__main__':
    unittest.main()