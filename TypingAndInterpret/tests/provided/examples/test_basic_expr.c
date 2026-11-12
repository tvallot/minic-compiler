#include "printlib.h"

int main() {
        println_int(42);
        println_int(3 - 2);
        println_int(-42);
        println_int(- -42);
        println_int(10 / 3);
        println_int(9 / 3);
        println_int(8 / 3);
        println_float(42.3);
        return 0;
}

// EXPECTED
// 42
// 1
// -42
// 42
// 3
// 3
// 2
// 42.30
