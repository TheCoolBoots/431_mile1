import sys
import json
import subprocess
from json_parser import parse
from type_checker import typeCheckProgram
from generateLLVM import toLLVM
from cfgToSSA import topSSACompile
from ast_class_definitions import m_prog

def top_compile(miniFile, outputFile = 'compilerOutput.ll', useMemory = False):

    ast = importMiniFile(miniFile)

    retType = typeCheckProgram(ast)

    if useMemory:
        if retType != -1:
            code = toLLVM(ast)

            print(code)
    else:
        if retType != -1:
            code = topSSACompile(ast)

            print(code)
    
def importMiniFile(filepath) -> m_prog:
    with open('tmp', 'w+') as outputHolder:
        subprocess.call(['java', '-jar', 'MiniCompiler.jar', filepath], stdout=outputHolder)

    jsonAST = ''
    with open('tmp', 'r') as outputHolder:
        jsonAST = json.load(outputHolder)

    return parse(jsonAST)

if __name__ == "__main__":
    if len(sys.argv) > 4:
        print(f'ERROR: got  {len(sys.argv)} arguments, expected <= 3')

    match sys.argv:
        case [pythonFile, miniFile]:
            top_compile(*sys.argv[1:])
        case [pythonFile, miniFile, outputFile]:
            top_compile(*sys.argv[1:])
        case [pythonFile, miniFile, outputFile, '-stack']:
            top_compile(*sys.argv[1:-1], useMemory=True)
        case [pythonFile, miniFile, '-stack']:
            top_compile(*sys.argv[1:-1], useMemory=True)

    # top_compile('miniFiles/dot.mini')