#include "printlib.h"

int main() {
        println_bool(1 == 1);
        println_bool(1 == 2);
        println_bool(1 != 1);
        println_bool(1 != 2);
        println_bool(1 < 2);
        println_bool(1 < 0);
        println_bool(1 <= 2);
        println_bool(1 <= 0);
        println_bool(1 > 2);
        println_bool(1 > 0);
        println_bool(1 >= 2);
        println_bool(1 >= 0);
        println_bool(!(1 < 2));
        return 0;
}

// EXPECTED
// 1
// 0
// 0
// 1
// 1
// 0
// 1
// 0
// 0
// 1
// 0
// 1
// 0
