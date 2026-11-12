#include "printlib.h"

int main() {
    int i;

    for (i = 5; ; i = i - 1) {
        println_int(i);
        println_int(50 / i);
    }

    return 0;
}

// EXPECTED
// 5
// 10
// 4
// 12
// 3
// 16
// 2
// 25
// 1
// 50
// 0
// Division by 0

// EXECCODE 1
// SKIP TEST EXPECTED