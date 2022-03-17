
import unittest
from top_compiler import toLLVM, importMiniFile

class test_top_compile(unittest.TestCase):
    def test_Fib(self):
        ast = importMiniFile('benchmark/Fibonacci/Fibonacci.mini')
        output = toLLVM(ast)
        print(output)

    def test_phiIf(self):
        ast = importMiniFile('analysisFiles/analysis1.mini')
        output = toLLVM(ast)
        print(output)



if __name__ == '__main__':
    unittest.main()