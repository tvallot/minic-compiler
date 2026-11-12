#include "printlib.h"

int main() {

    float x;

    x = 7.5 % 2.1;

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for non-integer modulo: float and float
// EXITCODE 2