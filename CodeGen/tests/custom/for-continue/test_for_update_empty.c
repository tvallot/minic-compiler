#include "printlib.h"

int main() {
    int i;

    for (i = 84; i < 90; ) {
        println_int(i);
        i = i + 2;
    }

    return 0;
}

// EXPECTED
// 84
// 86
// 88