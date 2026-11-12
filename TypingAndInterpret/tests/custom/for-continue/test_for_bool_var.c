#include "printlib.h"

int main() {
    int i;
    bool keep;

    keep = true;

    for (i = 120; keep; i = i + 7) {
        println_int(i);

        if (i > 135) {
            keep = false;
        }
    }

    return 0;
}

// EXPECTED
// 120
// 127
// 134
// 141