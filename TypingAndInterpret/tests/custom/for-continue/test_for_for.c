#include "printlib.h"

int main() {
    int i, j;

    for (i = 10; i < 13; i = i + 1) {
        for (j = 70; j < 73; j = j + 1) {
            println_int(i + j);
        }
    }

    return 0;
}

// EXPECTED
// 80
// 81
// 82
// 81
// 82
// 83
// 82
// 83
// 84