struct A{
    int b;
};

int a;
struct A* magic;

int main(void) {
    a = 5;
    struct A* aInst;
    struct A* bInst;
    aInst = bInst;
    return a;
}

// clang -c -emit-llvm tmp.c
// llvm-dis tmp.bc
