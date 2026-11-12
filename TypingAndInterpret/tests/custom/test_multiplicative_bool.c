#include "printlib.h"

int main() {

    bool x;

    x = true * false;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for multiplicative operands: boolean and boolean
// EXITCODE 2