#include "printlib.h"

int main() {
    int i;

    for (i = 4; ; ) {
        println_int(i);
        println_int(40 / i);
        i = i - 1;
    }

    return 0;
}

// EXPECTED
// 4
// 10
// 3
// 13
// 2
// 20
// 1
// 40
// 0
// Division by 0

// EXECCODE 1
// SKIP TEST EXPECTED