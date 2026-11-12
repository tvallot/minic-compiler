#include "printlib.h"

int main() {
    int i, j;
    i = 3;

    while (i < 7) {
        j = 2;
        while (j < 5) {
            println_int(i * j);
            j = j + 1;
        }
        i = i + 1;
    }

    return 0;
}

// EXPECTED
// 6
// 9
// 12
// 8
// 12
// 16
// 10
// 15
// 20
// 12
// 18
// 24