#include "printlib.h"

int main() {

    bool b;
    b = true;

    if (b) {
        println_int(12);
    }

    return 0;
}

// EXPECTED
// 12