#include "printlib.h"

int main() {
    int x, y, z;
    x = 84;
    y = 12;

    println_int(x / y);
    println_int(96 / y);
    println_int(x / 9);

    return 0;
}

// EXPECTED
// 7
// 8
// 9
