#include "printlib.h"

int main() {
    int i, sum;
    sum = 0;
    for (i = 1; i <= 10; i = i + 1) {
        if (i % 2 == 0) {
            continue;
        }
        sum = sum + i;
    }
    println_int(sum);
    return 0;
}
