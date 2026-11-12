#include <stdio.h>
/**
 * Compatibility layer with C (meant to be #included in MiniC source
 * files). Defines types, constants and functions that are built-in
 * MiniC, to allow compiling MiniC programs with GCC.
 */

typedef char * string;
/* Get definitions for bool type and true/false constants (exist since C99, but
   aren't always present by default). */
#include <stdbool.h>

void print_int(int);
void println_int(int);
void println_bool(int);

#define print_float(f) do { printf("%.2f", f); } while(0)
#define println_float(f) do { printf("%.2f\n", f); } while(0)

void print_string(string);
void println_string(string);
