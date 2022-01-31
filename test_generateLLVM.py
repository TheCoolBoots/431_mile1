import unittest
from ast_class_definitions import *
from generateLLVM import expressionToLLVM, statementToLLVM
import test_ast_trees

class test_LLVM_generation(unittest.TestCase):

    def test_conditional(self):
        ast = m_conditional(1, m_bool(True), [m_ret(1, m_num(3))], [m_ret(1, m_num(5))])

        

    def test_assignment(self):
        t_env = {'s1': [m_declaration(1, m_type('int'), m_id(1, 'a')), m_declaration(1, m_type('int'), m_id(1, 'b'))],
                's2': [m_declaration(1, m_type('int'), m_id(1, 'c')), m_declaration(1, m_type('s1'), m_id(1, 'struct1'))]}
        env = {'struct2_inst': m_type('s2'), 'z': m_type('int')}
        ast = m_assignment(1, [m_id(1,'struct2_inst'), m_id(1, 'struct1'), m_id(1, 'a')], m_id(1, 'z'))

        expected = []
        expected.append(f'%1 = load i64, i64* %z')
        expected.append(f'%2 = getelementptr %struct.s2, %struct.s2* %struct2_inst, i32 0, i32 1')
        expected.append(f'%3 = getelementptr %struct.s1, %struct.s1* %2, i32 0, i32 0')
        expected.append(f'store i64 %1, i64* %3')

        actual = statementToLLVM(0, ast, env, t_env, {})

        self.assertTrue(listsEqual(expected, actual[2]) and actual[1] == 'i64*' and actual[0]==3)

    def test_assignment_2(self):
        env = {'a':m_type('int')}
        ast = m_assignment(1, [m_id(1, 'a')], m_num(5))
        expected = [f'store i64 5, i64* %a']
        actual = statementToLLVM(0, ast, env, {}, {})
        self.assertTrue(actual[0] == 0 and actual[1] == 'i64*' and listsEqual(actual[2], expected))

    def test_assignment_3(self):
        t_env = {'bar': [m_declaration(1, m_type('int'), m_id(0,'bean'))]}
        env = {'z':m_type('bar'), 'a':m_type('bar')}
        ast = m_assignment(1, [m_id(1, 'z')], m_id(1, 'a')) # z = a

        expected = [f'%1 = load %struct.bar*, %struct.bar** %a', f'store %struct.bar* %1, %struct.bar** %z']
        actual = statementToLLVM(0, ast, env, t_env, {})

        self.assertTrue(actual[0] == 1 and actual[1] == f'%struct.bar*' and listsEqual(actual[2], expected))

    def test_type_declaration(self):
        self.assertEqual(test_ast_trees.structA8.getLLVM(), '%struct.A = type {i64, %struct.A*}')

    def test_unary(self):
        actual = expressionToLLVM(0, m_unary(3, '-', m_num(5)), {}, {}, {})
        expected = ['%1 = mul i64 -1, 5']
        self.assertTrue(listsEqual(actual[2], expected) and actual[0] == 1 and actual[1] == 'i64')

        actual = expressionToLLVM(0, m_unary(3, '!', m_bool(False)), {}, {}, {})
        expected = ['%1 = xor i64 1, 0']
        self.assertTrue(listsEqual(actual[2], expected) and actual[0] == 1 and actual[1] == 'i64')

        env = {'a': m_type('int')}

        actual = expressionToLLVM(0, m_unary(3, '-', m_id(2, 'a')), env, {}, {})
        expected = ['%1 = load i64, i64* %a', '%2 = mul i64 -1, %1']
        self.assertTrue(listsEqual(actual[2], expected) and actual[0] == 2  and actual[1] == 'i64')

        actual = expressionToLLVM(0, m_unary(3, '!', m_id(2, 'a')), env, {}, {})
        expected = ['%1 = load i64, i64* %a', '%2 = xor i64 1, %1']
        self.assertTrue(listsEqual(actual[2], expected) and actual[0] == 2 and actual[1] == 'i64')

    def test_binary(self):
        env = {'a': m_type('int')}

        actual = expressionToLLVM(0, m_binop(2, '==', m_bool(True), m_bool(False)), env, {}, {})
        expected = ['%1 = icmp eq i64 1, 0']
        self.assertTrue(listsEqual(actual[2], expected) and actual[0] == 1 and actual[1] == 'i64')

        actual = expressionToLLVM(0, m_binop(2, '==', m_id(2, 'a'), m_id(2, 'a')), env, {}, {})
        expected = ['%1 = load i64, i64* %a', '%2 = load i64, i64* %a', '%3 = icmp eq i64 %1, %2']
        self.assertTrue(actual[0] == 3 and actual[1] == 'i64' and listsEqual(actual[2], expected))

    def test_invocation(self):
        # function_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
        fun_env = {'FOO': (m_type('int'), [m_type('int')])}
        actual = expressionToLLVM(0, m_invocation(3, m_id(3, 'FOO'), [m_num(3)]), {}, {}, fun_env)
        expected = ['%1 = call i64 @FOO(i64 3)']
        self.assertTrue(actual[0] == 1 and actual[1] == 'i64' and listsEqual(actual[2], expected))

    def test_dot(self):
        t_env = {'s1': [m_declaration(1, m_type('int'), m_id(1, 'a')), m_declaration(1, m_type('int'), m_id(1, 'b'))],
                's2': [m_declaration(1, m_type('int'), m_id(1, 'c')), m_declaration(1, m_type('s1'), m_id(1, 'struct1'))]}
        env = {'struct2_inst': m_type('s2')}

        dot = m_dot(1, [m_id(1, 'struct2_inst'), m_id(1, 'struct1'), m_id(1, 'b')])


        expected = [f'%1 = getelementptr %struct.s2, %struct.s2* %struct2_inst, i32 0, i32 1',
                    f'%2 = getelementptr %struct.s1, %struct.s1* %1, i32 0, i32 1',
                    f'%3 = load i64, i64* %2']

        actual = expressionToLLVM(0, dot, env, t_env, {})
        self.assertTrue(listsEqual(actual[0] == 3 and actual[1] == 'i64' and actual[2], expected))

    def test_dot_2(self):
        env = {'a':m_type('int')}
        ast = m_dot(1, [m_id(1, 'a')])
        expected = [f'%1 = load i64, i64* %a']
        actual = expressionToLLVM(0, ast, env, {}, {})
        self.assertTrue(actual[0] == 1 and actual[1] == 'i64' and listsEqual(actual[2], expected))




if __name__ == '__main__':
    unittest.main()