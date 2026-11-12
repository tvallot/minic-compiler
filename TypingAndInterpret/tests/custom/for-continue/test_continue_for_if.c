#include "printlib.h"

int main() {

    int i;

    for (i = 90; i < 95; i = i + 1) {

        if (i == 92) {
            continue;
        }

        println_int(i);
    }

    return 0;
}

// EXPECTED
// 90
// 91
// 93
// 94