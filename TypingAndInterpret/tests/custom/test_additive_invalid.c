#include "printlib.h"

int main() {

    int x;

    x = 84 + true;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for additive operands: integer and boolean
// EXITCODE 2