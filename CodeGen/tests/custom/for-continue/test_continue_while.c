#include "printlib.h"

// continue in a while loop goes back to the condition.
int main() {
    int n;
    n = 0;

    while (n < 6) {
        n = n + 1;
        if (n % 2 == 0) {
            continue;
        }
        println_int(n);
    }

    return 0;
}

// EXPECTED
// 1
// 3
// 5
