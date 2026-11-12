#include "printlib.h"

int main() {

    bool x;

    x = !84;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for not expression: integer
// EXITCODE 2