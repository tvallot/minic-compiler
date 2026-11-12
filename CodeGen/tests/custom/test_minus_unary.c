#include "printlib.h"

int main() {
    int x;
    x = 64;

    println_int(-54);
    println_int(-x);
    println_int(-(-38));
    println_int(27 + -15);

    return 0;
}

// EXPECTED
// -54
// -64
// 38
// 12