#include "printlib.h"

int main() {
    bool a, b;
    a = true;
    b = false;

    println_bool(true && true);
    println_bool(true && false);
    println_bool(false && true);
    println_bool(false && false);

    println_bool(a && b);
    println_bool(a && true);
    println_bool(false && b);

    println_bool((42 > 30) && (18 < 10));
    println_bool((50 == 50) && (20 != 10));

    println_bool(true && true && true);
    println_bool(true && true && false);
    println_bool((42 > 10) && (30 > 20) && (5 > 2));

    return 0;
}

// EXPECTED
// 1
// 0
// 0
// 0
// 0
// 1
// 0
// 0
// 1
// 1
// 0
// 1