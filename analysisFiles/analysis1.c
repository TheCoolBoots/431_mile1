#include <stdio.h>

int main() {
    int check;
    check = 0;

    while (check < 100000) {

        if(check < 50000) {
            printf("1");
        }

        else {
            printf("2");
        }

       check = check + 1;
    }

    return check;
}