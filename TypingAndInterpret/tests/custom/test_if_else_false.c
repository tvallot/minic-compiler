#include "printlib.h"

int main(){
  int x;
  x = 25;

  if (x < 3) {
    println_int(33);
  } else {
    println_int(256);
  }

  return 0;
}

// EXPECTED
// 256