#include "printlib.h"

int main(){
  string n,m;
  n = "foo";
  m = "bar";
  println_string(n);
  println_string(m);
  println_string(n + m); // non-standard C
  return 0;
}

// SKIP TEST EXPECTED
// EXPECTED
// foo
// bar
// foobar
