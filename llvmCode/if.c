int main(void) {
    int a = 3;

    if(a == 2){
        return 3;
    }
    else{
        return 5;
    }
}

// clang -c -emit-llvm tmp.c
