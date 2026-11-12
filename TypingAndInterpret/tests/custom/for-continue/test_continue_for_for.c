#include "printlib.h"

int main() {
    int i, j;

    for (i = 11; i < 14; i = i + 1) {

        println_int(i);

        for (j = 51; j < 55; j = j + 1) {

            if (j == 53) {
                continue;
            }

            println_int(j);
        }
    }

    return 0;
}

// EXPECTED
// 11
// 51
// 52
// 54
// 12
// 51
// 52
// 54
// 13
// 51
// 52
// 54