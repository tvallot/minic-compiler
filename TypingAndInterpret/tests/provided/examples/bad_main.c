#include "printlib.h"

int toto(){
  println_int(42);
  return 0;
}

// SKIP TEST EXPECTED
// EXITCODE 5
// EXPECTED
// Functions are not supported in evaluation mode

