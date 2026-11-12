#include "printlib.h"

int main() {

    println_int(true);

    return 0;
}

// EXPECTED
// In function main: Line 5 col 4: invalid type for println_int statement: boolean
// EXITCODE 2