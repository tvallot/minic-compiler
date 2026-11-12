#include "printlib.h"

int main() {
    float x;

    for (x = 1.5; x < 5.0; x = x + 1.5) {
        println_float(x);
    }

    return 0;
}

// EXPECTED
// 1.50
// 3.00
// 4.50