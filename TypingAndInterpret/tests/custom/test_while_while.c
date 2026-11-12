#include "printlib.h"

int main() {

    int i, j;

    i = 0;

    while (i < 2) {

        j = 0;

        while (j < 3) {
            println_int(j);
            j = j + 1;
        }

        i = i + 1;
    }

    return 0;
}

// EXPECTED
// 0
// 1
// 2
// 0
// 1
// 2