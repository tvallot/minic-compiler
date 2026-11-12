# MiniC compiler

A small compiler, written in Python, for a subset of C. It turns a C
program into RISC-V assembly that runs on a RISC-V simulator.

I made it during the compilation course of my first year of master's
(Université Claude Bernard Lyon 1, 2025-2026).

## Example

Input (`examples/gcd.c`):

```c
#include "printlib.h"

int main() {
    int a, b, t;
    a = 1071;
    b = 462;
    while (b != 0) {
        t = b;
        b = a % b;
        a = t;
    }
    println_int(a);
    return 0;
}
```

Part of the generated RISC-V code (`while` loop):

```asm
lbl_begin_while_1_main:
        li t1, 0
        li t0, 0
        beq t5, t1, lbl_end_relational_3_main
        li t0, 1
lbl_end_relational_3_main:
        beq t0, zero, lbl_end_while_2_main
        mv t6, t5
        beq t5, zero, lbl_div_by_zero_0_main
        rem s11, t4, t5
        mv t5, s11
        mv t4, t6
        j lbl_begin_while_1_main
lbl_end_while_2_main:
        mv a0, t4
        call println_int
```

Running it in the simulator prints `21`.

## How it works

1. **Parsing**: the grammar is in `MiniC.g4`. ANTLR generates the lexer and
   the parser from it.
2. **Type checking** (`TypingAndInterpret/MiniCTypingVisitor.py`): rejects
   programs like `1 + true`, unknown variables, or `continue` outside a loop.
3. **Interpreter** (`TypingAndInterpret/MiniCInterpretVisitor.py`): runs the
   program directly on the syntax tree. Useful to check what the program
   should print.
4. **Code generation** (`CodeGen/MiniCCodeGen3AVisitor.py`): walks the syntax
   tree and produces three-address code, using an unlimited number of
   temporaries.
5. **Register allocation** (`CodeGen/`): replaces the temporaries with real
   RISC-V registers or stack slots. Three strategies:
   - `naive`: one register per temporary. Fails when there are more
     temporaries than registers.
   - `all-in-mem`: every temporary lives on the stack. Always works, but
     needs a load or store around each instruction.
   - `hybrid`: registers first, then the stack when there are no free
     registers left.

## The MiniC language

- types `int` and `bool` (`float` and `string` are also supported by the
  interpreter)
- arithmetic `+ - * / %`, comparisons, `&&`, `||`, `!`
- `if` / `else`, `while`, `for`, `continue`
- `println_int`, `println_bool`
- a single `main` function, no function calls, no arrays

`&&` and `||` are lazy like in C: in `x != 0 && 10 / x > 1`, the division is
not run when `x` is 0. A division by zero at runtime stops the program with
an error message.

## What I wrote

This project started from a code base given by the teacher of the course,
Matthieu Moy. He provided the
`Lib/` folder (RISC-V instructions, three-address code, stack frames), the
test runner and the base grammar.

My part:

- the type checker and the interpreter
- code generation for all expressions and statements
- the `all-in-mem` and `hybrid` register allocators
- the `for` loop and `continue` statement, from the grammar to the
  generated code
- the tests in `*/tests/custom/`

## Running it

You need Python 3.10+, ANTLR 4.13.2, the RISC-V GCC toolchain and the Spike
simulator. The easiest way is the Docker image used in the course, which
has everything:

```sh
docker run --rm -it -v "$PWD":/src -w /src mmoy/riscv-latex-python:dev bash
```

Then, inside the container:

```sh
make                                   # generate the parser
make run FILE=examples/gcd.c           # compile and run a program
make run FILE=examples/gcd.c ALLOC=all-in-mem

python3 MiniCC.py --mode eval examples/sum_odd.c                     # interpret
python3 MiniCC.py --mode codegen-linear --reg-alloc hybrid --stdout examples/gcd.c
```

## Tests

```sh
make test        # all tests
make typecheck   # static type checking with pyright
```

Each test is a `.c` file with the expected output written in comments:

```c
// EXPECTED
// 21
```

The test runner compiles each file with each allocator, runs it in Spike and
compares the output. It also compiles the file with GCC to check that the
expected output is correct. The tests run on GitHub Actions at each push.

- `*/tests/provided/`: tests given with the course
- `*/tests/custom/`: my tests

## Limitations

- Only one function (`main`), no function calls.
- No register allocation based on liveness analysis: the `hybrid` allocator
  gives registers in order, without checking which temporaries are still in
  use.
- The generated code is not optimized (for example, a comparison always
  produces a 0/1 value before the jump).
