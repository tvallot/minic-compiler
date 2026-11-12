#include "printlib.h"

// continue inside a while loop that is itself inside a for loop:
// it must go back to the while condition, not to the for update.
int main() {
    int i, j;

    for (i = 1; i < 3; i = i + 1) {
        j = 0;
        while (j < 4) {
            j = j + 1;
            if (j == 2) {
                continue;
            }
            println_int(i * 10 + j);
        }
        println_int(0);
    }

    return 0;
}

// EXPECTED
// 11
// 13
// 14
// 0
// 21
// 23
// 24
// 0
