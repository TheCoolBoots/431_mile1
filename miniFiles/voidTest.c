#include <stdlib.h>

struct A {
   int a;
   int b;
};

void deathSort() {
    return;
}

int main() {
    struct A a;
    int b;

    a = NULL;
    b = 1;

    a = deathSort();

    return 1;
}
