#include "printlib.h"

int main() {

    println_string(84);

    return 0;
}

// EXPECTED
// In function main: Line 5 col 4: invalid type for println_string statement: integer
// EXITCODE 2