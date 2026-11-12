#include "printlib.h"
int main() {
    println_int(54 - 33);
    println_int(51 - 0);
    println_int(54 - 33 - 10);
    println_int(54 - 60);
    return 0;
}
// EXPECTED
// 21
// 51
// 11
// -6