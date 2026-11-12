#include "printlib.h"

int main() {
    int i;
    i = 3;

    for (; ; i = i - 1) {
        println_int(i);
        println_int(30 / i);
    }

    return 0;
}

// EXPECTED
// 3
// 10
// 2
// 15
// 1
// 30
// 0
// Division by 0

// EXECCODE 1
// SKIP TEST EXPECTED