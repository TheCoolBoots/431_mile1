#include <stdio.h>
#include <stdlib.h>

int main(){

    printf("%d", 5);
    printf("%d\n", 5);
    scanf("%d");
    int* magic = (int*) malloc(sizeof(int));
    free(magic);
}