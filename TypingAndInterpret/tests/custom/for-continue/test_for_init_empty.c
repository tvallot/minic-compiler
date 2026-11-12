#include "printlib.h"

int main() {
    int i;
    i = 51;

    for (; i < 56; i = i + 1) {
        println_int(i);
    }

    return 0;
}

// EXPECTED
// 51
// 52
// 53
// 54
// 55