import unittest
from ast_class_definitions import *
from generateLLVM import expressionToLLVM, statementToLLVM
import test_ast_trees


top_env = {'b': (m_type('BIGCHUNGUS')), 'a': m_type('int'), 'MAGIC':m_type('bool')}
type_env = {'BIGCHUNGUS':[m_declaration(1, m_type('bool'), m_id(1, 'a'))]}
fun_env = {'BAR': (m_type('int'), [m_type('int'), m_type('int')]), 'FOO': (m_type('int'), [m_type('int')])}

class test_LLVM_generation(unittest.TestCase):

    def test_print(self):
        prnt = m_print(0, m_id(1, 'a'))
        expected = ['%t1 = load i32, i32* %a', 
                    '%t2 = call i32 @printf("%d", %t1)']
        actual = statementToLLVM(0, prnt, top_env, {}, {})
        self.assertEqual(expected, actual[2])

        prnt = m_print(0, m_num(2048))
        expected = ['%t1 = call i32 @printf("%d", 2048)']
        actual = statementToLLVM(0, prnt, top_env, {}, {})
        self.assertEqual(expected, actual[2])

    def test_conditional(self):
        ast = m_conditional(1, m_id(5, 'MAGIC'), [m_ret(1, m_num(3))], [m_ret(1, m_num(5))])
        expected = ['%t1 = load i32, i32* %MAGIC',
                    'br i1 %t1, label %l2, label %l3',
                    'l2:',
                    'ret i32 3',
                    'br label %l4',
                    'l3:',
                    'ret i32 5',
                    'br label %l4',
                    'l4:']
        actual = statementToLLVM(0, ast, top_env, type_env, fun_env)

        self.assertEqual(expected, actual[2])
        self.assertEqual(actual[1], 'i32')
        self.assertEqual(actual[0], 4)

    
    def test_conditional2(self):
        ast = m_conditional(1, m_bool(True), [m_ret(1, m_num(3))], [m_ret(1, m_num(5))])
        expected = ['br i1 1, label %l1, label %l2',
                    'l1:',
                    'ret i32 3',
                    'br label %l3',
                    'l2:',
                    'ret i32 5',
                    'br label %l3',
                    'l3:']
        actual = statementToLLVM(0, ast, top_env, type_env, fun_env)

        self.assertEqual(expected, actual[2])
        self.assertEqual(actual[1], 'i32')
        self.assertEqual(actual[0], 3)


    def test_loop(self):
        ast = m_loop(1, m_bool(True), [m_ret(1, m_num(3))])
        expected = ['l1:',
                    'br i1 1, label %l2, label %l3',
                    'l2:',
                    'ret i32 3',
                    'br label %l1',
                    'l3:']

        actual = statementToLLVM(0, ast, {}, {}, {})
        self.assertEqual(expected, actual[2])
        self.assertEqual(actual[1], 'i32')
        self.assertEqual(actual[0], 3)

    def test_loop2(self):
        ast = m_loop(1, m_id(81913, 'MAGIC'), [m_ret(1, m_num(3))])
        expected = ['%t1 = load i32, i32* %MAGIC',
                    'l2:',
                    'br i1 %t1, label %l3, label %l4',
                    'l3:',
                    'ret i32 3',
                    'br label %l2',
                    'l4:']

        actual = statementToLLVM(0, ast, top_env, {}, {})
        self.assertEqual(expected, actual[2])
        self.assertEqual(actual[1], 'i32')
        self.assertEqual(actual[0], 4)

    def test_assignment(self):
        t_env = {'s1': [m_declaration(1, m_type('int'), m_id(1, 'a')), m_declaration(1, m_type('int'), m_id(1, 'b'))],
                's2': [m_declaration(1, m_type('int'), m_id(1, 'c')), m_declaration(1, m_type('s1'), m_id(1, 'struct1'))]}
        env = {'struct2_inst': m_type('s2'), 'z': m_type('int')}
        ast = m_assignment(1, [m_id(1,'struct2_inst'), m_id(1, 'struct1'), m_id(1, 'a')], m_id(1, 'z'))
        """
        struct s2 struct2_inst;
        int z;
        struct2_inst.struct1.a = z
        """

        expected = []
        expected.append(f'%t1 = load i32, i32* %z')
        expected.append(f'%t2 = getelementptr %struct.s2, %struct.s2* %struct2_inst, i32 0, i32 1')
        expected.append(f'%t3 = getelementptr %struct.s1, %struct.s1* %t2, i32 0, i32 0')
        expected.append(f'store i32 %t1, i32* %t3')

        actual = statementToLLVM(0, ast, env, t_env, {})

        self.assertEqual(expected, actual[2])


    def test_assignment_2(self):
        env = {'a':m_type('int')}
        ast = m_assignment(1, [m_id(1, 'a')], m_num(5))
        """
        int a;
        a = 5;
        """
        expected = [f'store i32 5, i32* %a']
        actual = statementToLLVM(0, ast, env, {}, {})
        self.assertEqual(actual[2], expected)


    def test_assignment_3(self):
        t_env = {'bar': [m_declaration(1, m_type('int'), m_id(0,'bean'))]}
        env = {'z':m_type('bar'), 'a':m_type('bar')}
        ast = m_assignment(1, [m_id(1, 'z')], m_id(1, 'a')) 
        """
        struct bar z;
        struct bar a;
        z = a;
        """

        expected = [f'%t1 = add %struct.bar* %a, 0', '%z = add %struct.bar* %t1, 0']
        actual = statementToLLVM(0, ast, env, t_env, {})

        self.assertEqual(actual[2], expected)

    def test_assignment4(self):
        t_env = {'s1': [m_declaration(1, m_type('int'), m_id(1, 'a')), m_declaration(1, m_type('int'), m_id(1, 'b'))],
                's2': [m_declaration(1, m_type('int'), m_id(1, 'c')), m_declaration(1, m_type('s1'), m_id(1, 'struct1'))]}
        env = {'struct2_inst': m_type('s2'), 'struct1_inst': m_type('s1')}
        ast = m_assignment(1, [m_id(1,'struct2_inst'), m_id(1, 'struct1')], m_id(1, 'struct1_inst'))
        """
        struct s2 struct2_inst;
        struct s1 struct1_inst;
        struct2_inst.struct1 = struct1_inst
        """

        expected = []
        # expected.append(f'%1 = %struct.s1* %struct1_inst')
        expected.append(f'%t1 = add %struct.s1* %struct1_inst, 0')
        expected.append(f'%t2 = getelementptr %struct.s2, %struct.s2* %struct2_inst, i32 0, i32 1')
        expected.append(f'store %struct.s1* %t1, %struct.s1** %t2')

        actual = statementToLLVM(0, ast, env, t_env, {})

        self.assertEqual(expected, actual[2])


    def test_type_declaration(self):
        self.assertEqual(test_ast_trees.structA8.getLLVM(), '%struct.A = type {i32, %struct.A*}')


    def test_unary(self):
        actual = expressionToLLVM(0, m_unary(3, '-', m_num(5)), {}, {}, {})
        expected = ['%t1 = mul i32 -1, 5']
        self.assertTrue(actual[0] == 1 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)

        actual = expressionToLLVM(0, m_unary(3, '!', m_bool(False)), {}, {}, {})
        expected = ['%t1 = xor i1 1, 0']
        self.assertTrue(actual[0] == 1 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)

        env = {'a': m_type('int')}

        actual = expressionToLLVM(0, m_unary(3, '-', m_id(2, 'a')), env, {}, {})
        expected = ['%t1 = load i32, i32* %a', 
                    '%t2 = mul i32 -1, %t1']
        self.assertTrue(actual[0] == 2  and actual[1] == 'i32')
        self.assertEqual(actual[2], expected) 

        actual = expressionToLLVM(0, m_unary(3, '!', m_id(2, 'a')), env, {}, {})
        expected = ['%t1 = load i32, i32* %a', 
                '%t2 = xor i1 1, %t1']
        self.assertTrue(actual[0] == 2 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)


    def test_binary(self):
        env = {'a': m_type('int')}

        actual = expressionToLLVM(0, m_binop(2, '==', m_bool(True), m_bool(False)), env, {}, {})
        expected = ['%t1 = icmp eq i1 1, 0']
        self.assertTrue(actual[0] == 1 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)

        actual = expressionToLLVM(0, m_binop(2, '==', m_id(2, 'a'), m_id(2, 'a')), env, {}, {})
        expected = ['%t1 = load i32, i32* %a', 
                    '%t2 = load i32, i32* %a', 
                    '%t3 = icmp eq i1 %t1, %t2']
        self.assertTrue(actual[0] == 3 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)


    def test_invocation(self):
        # function_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
        actual = expressionToLLVM(0, m_invocation(3, m_id(3, 'FOO'), [m_num(3)]), {}, {}, fun_env)
        expected = ['%t1 = call i32 @FOO(i32 3)']
        self.assertTrue(actual[0] == 1 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)

        invocation = m_invocation(3, m_id(3, 'FOO'), [m_id(2, 'a')])
        actual = expressionToLLVM(0, invocation, top_env, type_env, fun_env)
        expected = ['%t1 = load i32, i32* %a',
                    '%t2 = call i32 @FOO(i32 %t1)']

        self.assertEqual(actual[2], expected)
        self.assertEqual(actual[0], 2)
        self.assertEqual(actual[1], 'i32')


    def test_dot(self):
        t_env = {'s1': [m_declaration(1, m_type('int'), m_id(1, 'a')), m_declaration(1, m_type('int'), m_id(1, 'b'))],
                's2': [m_declaration(1, m_type('int'), m_id(1, 'c')), m_declaration(1, m_type('s1'), m_id(1, 'struct1'))]}
        env = {'struct2_inst': m_type('s2')}

        dot = m_dot(1, [m_id(1, 'struct2_inst'), m_id(1, 'struct1'), m_id(1, 'b')])


        expected = [f'%t1 = getelementptr %struct.s2, %struct.s2* %struct2_inst, i32 0, i32 1',
                    f'%t2 = getelementptr %struct.s1, %struct.s1* %t1, i32 0, i32 1',
                    f'%t3 = load i32, i32* %t2']

        actual = expressionToLLVM(0, dot, env, t_env, {})
        self.assertTrue(actual[0] == 3 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)


    def test_dot_2(self):
        env = {'a':m_type('int')}
        ast = m_dot(1, [m_id(1, 'a')])
        expected = [f'%t1 = load i32, i32* %a']
        actual = expressionToLLVM(0, ast, env, {}, {})
        self.assertTrue(actual[0] == 1 and actual[1] == 'i32')
        self.assertEqual(actual[2], expected)


    def test_ret(self):
        ret1 = m_ret(169, m_id(5, 'a'))
        expected1 = [f'%t1 = load i32, i32* %a', 'ret i32 %t1']
        actual1 = statementToLLVM(0, ret1, top_env, type_env, fun_env)
        self.assertEqual(expected1, actual1[2])

        ret2 = m_ret(420)
        expected2 = [f'ret void']
        actual2 = statementToLLVM(0, ret2, top_env, type_env, fun_env)
        self.assertEqual(expected2, actual2[2])

        ret3 = m_ret(9001, m_new_struct(m_id(3, 'BIGCHUNGUS')))
        expected3 = ['%t1 = call i8* @malloc(4)', 
                        '%t1 = bitcast i8* %t1 to %struct.BIGCHUNGUS*', 
                        f'ret %struct.BIGCHUNGUS* %t1']
        actual3 = statementToLLVM(0, ret3, top_env, type_env, fun_env)
        self.assertEqual(expected3, actual3[2])


if __name__ == '__main__':
    unittest.main()