#include "printlib.h"
int main() {
    int x, y;
    x = 6;
    y = 7;
    println_int(x * y);
    println_int(x * 2);
    println_int(3 * y);
    return 0;
}
// EXPECTED
// 42
// 12
// 21