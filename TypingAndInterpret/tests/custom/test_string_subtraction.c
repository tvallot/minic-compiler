#include "printlib.h"

int main() {

    string x;

    x = "abc" - "def";

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for additive operands: string and string
// EXITCODE 2