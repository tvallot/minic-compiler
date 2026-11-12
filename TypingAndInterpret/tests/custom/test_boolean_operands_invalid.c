#include "printlib.h"

int main() {

    bool x;

    x = true || 84;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for boolean operands: boolean and integer
// EXITCODE 2