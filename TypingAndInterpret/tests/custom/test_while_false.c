#include "printlib.h"

int main() {

    bool b;
    b = false;

    while (b) {
        println_int(12);
    }

    return 0;
}

// EXPECTED