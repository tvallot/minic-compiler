#include "printlib.h"

int main() {

    while (84) {
        println_int(12);
    }

    return 0;
}

// EXPECTED
// In function main: Line 5 col 4: invalid type for while condition: integer
// EXITCODE 2