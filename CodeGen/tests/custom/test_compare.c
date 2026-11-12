#include "printlib.h"

int main() {

    println_bool(42 < 57);
    println_bool(64 <= 64);
    println_bool(91 > 18);
    println_bool(73 >= 73);
    println_bool(55 == 55);
    println_bool(28 != 39);

    println_bool(57 < 42);
    println_bool(65 <= 64);
    println_bool(18 > 91);
    println_bool(72 >= 73);
    println_bool(55 == 56);
    println_bool(28 != 28);

    return 0;
}

// EXPECTED
// 1
// 1
// 1
// 1
// 1
// 1
// 0
// 0
// 0
// 0
// 0
// 0