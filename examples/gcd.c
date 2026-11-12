#include "printlib.h"

int main() {
    int a, b, t;
    a = 1071;
    b = 462;
    while (b != 0) {
        t = b;
        b = a % b;
        a = t;
    }
    println_int(a);
    return 0;
}
