import unittest
from ast_class_definitions import *
from generateLLVM import expressionToLLVM
import test_ast_trees

class test_LLVM_generation(unittest.TestCase):

    def test_type_declaration(self):
        self.assertEqual(test_ast_trees.structA8.getLLVM(), '%struct.A = type {i64, %struct.A*}')

    def test_unary(self):
        actual = expressionToLLVM(0, m_unary(3, '-', m_num(5)), {})
        expected = ['%tmp1 = mul i64 -1, 5']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 1)

        actual = expressionToLLVM(0, m_unary(3, '!', m_bool(False)), {})
        expected = ['%tmp1 = xor i64 1, 0']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 1)

        actual = expressionToLLVM(0, m_unary(3, '-', m_id(2, 'a')), {})
        expected = ['%tmp1 = load i64* %a', '%tmp2 = mul i64 -1, %tmp1']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 2)

        actual = expressionToLLVM(0, m_unary(3, '!', m_id(2, 'a')), {})
        expected = ['%tmp1 = load i64* %a', '%tmp2 = xor i64 1, %tmp1']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 2)

    def test_binary(self):
        actual = expressionToLLVM(0, m_binop(2, '==', m_bool(True), m_bool(False)), {})
        expected = ['%tmp1 = icmp eq i64 1, 0']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 1)

        actual = expressionToLLVM(0, m_binop(2, '==', m_id(2, 'a'), m_id(2, 'a')), {})
        expected = ['%tmp1 = load i64* %a', '%tmp2 = load i64* %a', '%tmp3 = icmp eq i64 %tmp1, %tmp2']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 3)

    def test_invocation(self):
        # function_env structure: {str: (m_type, list[m_type])}     maps funID -> return type
        fun_env = {'FOO': (m_type('int'), [m_type('int')])}
        actual = expressionToLLVM(0, m_invocation(3, m_id(3, 'FOO'), [m_num(3)]), fun_env)
        expected = ['%tmp1 = call i64 @FOO(i64 3)']
        self.assertTrue(listsEqual(actual[1], expected) and actual[0] == 1)

if __name__ == '__main__':
    unittest.main()