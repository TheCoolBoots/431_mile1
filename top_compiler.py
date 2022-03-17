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
    code.append('target datalayout = "e-m:o-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"')
    code.append('target triple = "x86_64-apple-macosx10.15.0')

    code.extend(['declare align 16 i8* @malloc(i32) #2', 
                'declare void @free(i8*) #1', 
                'declare i32 @printf(i8*, ...) #1', 
                'declare i32 @scanf(i8*, ...) #1', 
                '@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1',
                '@.str.1 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1'])

    if useMemory:
        if retType != -1:
            code.extend(toLLVM(ast))
        else:
            return
    else:
        if retType != -1:
            code.extend(topSSACompile(ast))
        else:
            return
    
    code.extend(['attributes #0 = { noinline nounwind optnone ssp uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }',
                'attributes #1 = { allocsize(0) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="penryn" "target-features"="+cx16,+cx8,+fxsr,+mmx,+sahf,+sse,+sse2,+sse3,+sse4.1,+ssse3,+x87" "tune-cpu"="generic" }',
                'attributes #2 = { allocsize(0) }',
                '!llvm.module.flags = !{!0, !1, !2, !3}',
                '!llvm.ident = !{!4}',
                '!0 = !{i32 1, !"wchar_size", i32 4}',
                '!1 = !{i32 7, !"PIC Level", i32 2}',
                '!2 = !{i32 7, !"uwtable", i32 1}',
                '!3 = !{i32 7, !"frame-pointer", i32 2}',
                '!4 = !{!"Homebrew clang version 13.0.1"}'])

    print('\n'.join(code))

    return '\n'.join(code)


    
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
        case[pythonFile, miniFile, '-stack']:
            top_compile(*sys.argv[1:-1], useMemory=True)
        case [pythonFile, miniFile, outputFile]:
            top_compile(*sys.argv[1:])
        case [pythonFile, miniFile, outputFile, '-stack']:
            top_compile(*sys.argv[1:-1], useMemory=True)

    # top_compile('miniFiles/dot.mini')