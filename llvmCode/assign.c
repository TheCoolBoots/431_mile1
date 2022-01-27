struct A{
    int b;
};
int main(void) {
    struct A* aInst;
    struct A* bInst;
    aInst = bInst;
}

// clang -c -emit-llvm tmp.c
// llvm-dis tmp.bc
