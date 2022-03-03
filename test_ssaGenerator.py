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

        node = CFG_Node(0, 'statement block node')
        node.ast_statements = statementList

        # %1 = i32 42
        # %2 = add i32 %1, i32 %1
        # %3 = i32 23
        # %4 = add i32 %2, i32 %3

        lastRegUsed, code = generateSSA(0, node, {}, {}, {})
        expectedMappings = {'a': ('i32', 2, 0), 'b': ('i32_immediate', 42, 0), 'c': ('i32', 1, 0)}
        expected = ['%t1 = add i32 42, 42', '%t2 = add i32 %t1, 23']
        self.assertEqual(code, expected)
        self.assertEqual(expectedMappings, node.mappings)


    # t_env structure: {str: list[m_declaration]}
    def test_legacy(self):
        ast = importMiniFile('ssaFormFiles/legacy.mini')
        statementList = ast.functions[0].statements

        node = CFG_Node(0, 'statement block node')
        node.ast_statements = statementList

        types = {'A':[m_declaration(1, m_type('int'), m_id(1, 'a'))]}

        env = {'varHolder': (False, m_type('A'))}

        lastRegUsed, code = generateSSA(0, node, env, types, {})
        expected = ['%t1 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0', 
                    'store i32 1, i32* %t1', 
                    '%t2 = getelementptr %struct.A, %struct.A* %varHolder, i32 0, i32 0', 
                    '%t3 = load i32, i32* %t2', 
                    '%t4 = call i32 @printf("%d", %t3)', 
                    '%t5 = load %struct.A** %varHolder', 
                    '%t6 = bitcast %struct.A* %t5 to i8*', 
                    'call void @free(%t6)']

        self.assertEqual(code, expected)

    def test_return(self):
        ast = importMiniFile('ssaFormFiles/return.mini')
        statementList = ast.functions[0].statements
        node = CFG_Node(0, 'statement block node')
        node.ast_statements = statementList
        functions = {'foo':(m_type('void'), [m_type('int')])}

        expected = ['%t1 = call void @foo(i32 5)',
                    '%t0 = void',
                    'br label %retLabel']

        lastRegUsed, code = generateSSA(0, node, {}, {}, functions)
        self.assertEqual(code, expected)
        # mappings structure = {str id: (str llvmType, int regNum, str m_typeID)}

    def test_globals(self):
        ast = importMiniFile('ssaFormFiles/globals.mini')
        statements = ast.functions[0].statements
        node = CFG_Node(0, 'statement block node')
        node.ast_statements = statements
        top_env = ast.getTopEnv(includeLineNum=False)
        types = ast.getTypes()

        expected = ['store i32 5, i32* @a', 
                    'store i32 4, i32* @b', 
                    '%t1 = load i32* @a', 
                    '%t2 = load i32* @b', 
                    '%t3 = add i32 %t1, %t2', 
                    '%t0 = add i32 %t3, 0',
                    'br label %retLabel']

        lastRegUsed, code = generateSSA(0, node, top_env, types, {})

        # print('\n'.join(code))

        self.assertEqual(expected,code)
        # self.assertEqual(node.mappings, {})

    def test_structs(self):
        ast = importMiniFile('ssaFormFiles/structs.mini')
        statements = ast.functions[0].statements
        localDeclarations = ast.functions[0].body_declarations
        top_env = ast.getTopEnv()
        types = ast.getTypes()

        node = CFG_Node(0, 'statement block node')
        node.ast_statements = statements

        for localDec in localDeclarations:
            top_env[localDec.id.identifier] = (False, localDec.type)

        lastRegUsed, code = generateSSA(0, node, top_env, types, {})

        expected =['%t1 = call i8* @malloc(8)', 
                    '%t1 = bitcast i8* %t1 to %struct.A*', 
                    'store %struct.A* %t1, %struct.A** %redacted', 
                    '%t2 = call i8* @malloc(8)', 
                    '%t2 = bitcast i8* %t2 to %struct.A*',
                    'store %struct.A* %t2, %struct.A** @beoch', 
                    '%t3 = getelementptr %struct.A, %struct.A* @beoch, i32 0, i32 0', 
                    '%t4 = load i32, i32* %t3', 
                    '%t0 = add i32 %t4, 0',
                    'br label %retLabel']

        self.assertEqual(code, expected)

        declarationCode = []
        for globalDec in ast.global_declarations:
            declarationCode.append(globalDec.getSSAGlobals())
        
        for localDec in localDeclarations:
            declarationCode.append(localDec.getSSALocals())

        expectedDecls = ['@beoch = common dso_local global %struct.A* null', '%redacted = alloca %struct.A*']
        self.assertEqual(declarationCode, expectedDecls)

        

if __name__ == '__main__':
    unittest.main()