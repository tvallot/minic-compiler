#include "printlib.h"

int main() {

    int i;

    for (i = 0; i < 3; i = i + 1) {
    }

    println_int(i);

    return 0;
}

// EXPECTED
// 3