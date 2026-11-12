#include "printlib.h"

int main() {

    bool x;

    x = "abc" < "def";

    return 0;
}

// EXPECTED
// In function main: Line 7 col 8: invalid type for relational operands: string and string
// EXITCODE 2