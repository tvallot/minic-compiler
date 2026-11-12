#include "printlib.h"

int main() {
    bool a, b;
    a = true;
    b = false;

    // constants
    println_bool(true || true);
    println_bool(true || false);
    println_bool(false || true);
    println_bool(false || false);

    // variables
    println_bool(a || b);
    println_bool(a || false);
    println_bool(false || b);

    // mixed with comparisons
    println_bool((42 > 30) || (18 < 10));
    println_bool((50 == 40) || (20 != 10));

    println_bool(true || false || false);
    println_bool(false || false || false);
    println_bool((42 > 10) || (5 > 20) || (3 > 1));

    return 0;
}

// EXPECTED
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
// 0
// 1