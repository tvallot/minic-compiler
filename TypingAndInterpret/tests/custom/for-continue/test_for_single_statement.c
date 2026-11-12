#include "printlib.h"

int main() {
    int i;

    for (i = 41; i < 46; i = i + 2)
        println_int(i);

    return 0;
}

// EXPECTED
// 41
// 43
// 45