#include "printlib.h"

int main() {
    bool a, b;

    a = true;
    b = false;

    println_bool(!a);
    println_bool(!b);
    println_bool(!true);
    println_bool(!false);
    println_bool(!!true);
    println_bool(!!!false);
    println_bool(!(3 < 2));
    println_bool(!(4 == 4));
    println_bool(!((5 > 2) && (1 < 0)));

    return 0;
}

// EXPECTED
// 0
// 1
// 0
// 1
// 1
// 1
// 1
// 0
// 1