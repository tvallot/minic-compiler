#include "printlib.h"

// && and || must not evaluate their right side when the result is
// already known (otherwise the division by zero would stop the program).
int main() {
    int x, zero;
    x = 10;
    zero = 0;

    println_bool(zero != 0 && x / zero > 1);
    println_bool(zero == 0 || x / zero > 1);
    println_bool(x > 5 && x % 3 == 1);
    println_bool(x < 5 || x == 10);

    return 0;
}

// EXPECTED
// 0
// 1
// 1
// 1
