struct s1 {
    int a;
    int b;
};

struct s2 {
    int c;
    struct s1 struct1;
};

int main(void) {
    struct s2 struct2_inst;
    struct2_inst.struct1.b = 10;
    struct2_inst.struct1.a = 3;
}
