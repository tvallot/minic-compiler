#include "printlib.h"

int main() {

    if (51) {
        println_int(12);
    }

    return 0;
}

// EXPECTED
// In function main: Line 5 col 4: invalid type for if condition: integer
// EXITCODE 2