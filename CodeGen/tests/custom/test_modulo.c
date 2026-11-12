#include "printlib.h"
int main() {
    println_int(33 % 6);
    println_int(33 % 33);
    println_int(33 % 55);
    println_int(47 % 8);
    println_int(-33 % 6);
    println_int(33 % -6);
    return 0;
}
// EXPECTED
// 3
// 0
// 33
// 7
// -3
// 3