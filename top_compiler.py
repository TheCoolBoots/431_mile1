import sys
import json
import subprocess
from json_parser import parse
from type_checker import typeCheckProgram
from generateLLVM import toLLVM
from ast_class_definitions import m_prog

def top_compile(miniFile, outputFile = 'compilerOutput.ll'):

    ast = importMiniFile(miniFile)

    retType = typeCheckProgram(ast)

    if retType != -1:
        code = toLLVM(ast)

        print(code)
    
def importMiniFile(filepath) -> m_prog:
    with open('tmp', 'w+') as outputHolder:
        subprocess.call(['java', '-jar', 'MiniCompiler.jar', filepath], stdout=outputHolder)

    jsonAST = ''
    with open('tmp', 'r') as outputHolder:
        jsonAST = json.load(outputHolder)

    return parse(jsonAST)

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(f'ERROR: got  {len(sys.argv)} arguments, expected <= 3')

    # print(*sys.argv[1:])
    top_compile(*sys.argv[1:])
    # top_compile('miniFiles/dot.mini')