#include "printlib.h"

int main(){
  println_bool(true+true);
  return 0;
}
// EXITCODE 2
// EXPECTED
// In function main: Line 4 col 15: invalid type for additive operands: boolean and boolean
