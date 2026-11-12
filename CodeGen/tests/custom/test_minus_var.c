#include "printlib.h"

int main() {
    int x, y;
    x = 70;
    y = 25;

    println_int(x - y);
    println_int(x - 15);
    println_int(90 - y);

    return 0;
}

// EXPECTED
// 45
// 55
// 65