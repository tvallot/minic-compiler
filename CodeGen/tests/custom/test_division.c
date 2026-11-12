#include "printlib.h"
int main() {
    println_int(40 / 5);
    println_int(15 / 6);
    println_int(5 / 40);
    println_int(-40 / 5);
    println_int(40 / -5);
    println_int(84 / 7 / 3);

    return 0;
}
// EXPECTED
// 8
// 2
// 0
//-8
//-8
// 4