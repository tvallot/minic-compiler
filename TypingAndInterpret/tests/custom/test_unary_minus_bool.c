#include "printlib.h"

int main() {

    bool x;

    x = -true;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for unary minus operand: boolean
// EXITCODE 2