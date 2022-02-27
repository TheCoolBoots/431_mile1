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

    code = []
    # These can change a lot depending on how its compiled
    code.append("; ModuleID = 'PLACEHOLDER_NAME.bc'")
    code.append('source_filename = "PLACEHOLDER_NAME.c"') # This could probably be changed to .mini if that doesnt cause a problem
    code.append('target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"')
    code.append('target triple = "x86_64-pc-linux-gnu"')

    if useMemory:
        if retType != -1:
            code.extend(toLLVM(ast))
    else:
        if retType != -1:
            code.extend(topSSACompile(ast))

    # This string will often come before functions in llvm, not sure if it is needed, may need to parse thru and add it.
    # code.insert(index, "; Function Attrs: noinline nounwind optnone ssp uwtable")

    code.append('attributes  # 0 = { noinline nounwind optnone uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "frame-pointer"="all" "less-precise-fpmad"="false" "min-legal-vector-width"="0" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }')
    # These last 4 lines can change a lot depending how its compiled, not sure how important it actually is
    code.append('!llvm.module.flags = !{!0}')
    code.append('!llvm.ident = !{!1}')
    code.append('!0 = !{i32 1, !"wchar_size", i32 4}')
    code.append('!1 = !{!"clang version 10.0.0-4ubuntu1 "}')



    
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