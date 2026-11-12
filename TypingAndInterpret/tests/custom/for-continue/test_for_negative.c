#include "printlib.h"

int main() {
    int i;

    for (i = 314; 84; i = i + 1) {
        println_int(i);
    }

    return 0;
}

// EXPECTED
// In function main: Line 6 col 4: invalid type for for condition: integer
// EXITCODE 2