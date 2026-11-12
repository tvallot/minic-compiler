#include "printlib.h"

int main(){
  println_int(21/ 0);
  return 0;
}

// EXPECTED
// Division by 0
// EXECCODE 1
// SKIP TEST EXPECTED