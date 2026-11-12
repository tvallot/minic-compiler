#include "printlib.h"

int main() {
    int x, y;
    x = 83;
    y = 12;

    println_int(x % y);
    println_int(95 % y);
    println_int(x % 9);
    println_int(84 % y);

    return 0;
}

// EXPECTED
// 11
// 11
// 2
// 0