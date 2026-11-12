#include "printlib.h"

int main() {

    int i;
    i = 3;

    while (true) {
        println_int(i);
        println_int(30 / i);
        i = i - 1;
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