#include <stdio.h>

int main() {
    int check;
    int val1;
    int val2;
    check = 0;
    val1 = 0;
    val2 = 0;


    while (check < 100000) {

        if(check < 50000) {
            val1 = val1 + 1;
        }

        else {
            val2 = val2 + 1;
        }

       check = check + 1;
    }

    return check;
}