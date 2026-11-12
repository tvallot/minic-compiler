#include "printlib.h"

int main() {
    int i, j;
    i = 3;

    for(i = 1; i < 7; i = i + 1) {
        println_int(i);
    }

    return 0;
}

// EXPECTED
// 1
// 2
// 3
// 4
// 5
// 6