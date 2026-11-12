#include "printlib.h"

int main(){
  int i;
  i = 0;

  while (i < 6) {
    println_int(i);
    i = i + 1;
  }

  return 0;
}

// EXPECTED
// 0
// 1
// 2
// 3
// 4
// 5