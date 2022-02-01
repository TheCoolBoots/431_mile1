import sys
import json
import subprocess
from json_parser import parse
from type_checker import typeCheckProgram
from generateLLVM import toLLVM

def top_compile(miniFile, outputFile = 'compilerOutput.ll'):

    with open('tmp', 'w+') as outputHolder:
        subprocess.call(['java', '-jar', 'miniFiles/MiniCompiler.jar', miniFile], stdout=outputHolder)

    jsonAST = ''
    with open('tmp', 'r') as outputHolder:
        jsonAST = json.load(outputHolder)

    ast = parse(jsonAST)

    retType = typeCheckProgram(ast)

    code = toLLVM(ast)

    print(code)
    


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(f'ERROR: got  {len(sys.argv)} arguments, expected <= 3')

    top_compile(*sys.argv[1:])
    # top_compile('miniFiles/structs.mini')