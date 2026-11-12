#include "printlib.h"

int main() {
    int i;

    for (i = 10; i < 16; i = i + 1) {

        if (i == 13) {
            continue;
        }

        println_int(i);
    }

    return 0;
}

// EXPECTED
// 10
// 11
// 12
// 14
// 15