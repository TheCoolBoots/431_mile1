#include <stdio.h>
#include <stdlib.h>

int main(){

    printf("%d", 5);
    printf("%d\n", 5);
    int a;
    scanf("%d", &a);
    int* magic = (int*) malloc(sizeof(int));
    free(magic);
}