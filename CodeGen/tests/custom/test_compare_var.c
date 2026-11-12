#include "printlib.h"

int main() {
    int x, y;
    x = 48;
    y = 31;

    println_bool(x > y);
    println_bool(x > 40);
    println_bool(60 > x);

    println_bool(x < y);
    println_bool(y < 40);
    println_bool(20 < y);

    println_bool(x >= y);
    println_bool(x >= 48);
    println_bool(52 >= x);

    println_bool(x <= y);
    println_bool(y <= 31);
    println_bool(40 <= x);

    println_bool(x == y);
    println_bool(x == 48);
    println_bool(31 == y);

    println_bool(x != y);
    println_bool(x != 50);
    println_bool(40 != y);

    return 0;
}

// EXPECTED
// 1
// 1
// 1
// 0
// 1
// 1
// 1
// 1
// 1
// 0
// 1
// 1
// 0
// 1
// 1
// 1
// 1
// 1