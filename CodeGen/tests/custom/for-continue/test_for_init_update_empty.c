#include "printlib.h"

int main() {
    int i;
    i = 200;

    for (; i < 206; ) {
        println_int(i);
        i = i + 3;
    }

    return 0;
}

// EXPECTED
// 200
// 203