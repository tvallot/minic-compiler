#! /usr/bin/env python3
"""
MiniC compiler: command line entry point.

Usage:
    python3 MiniCC.py --mode eval program.c
    python3 MiniCC.py --mode codegen-linear --reg-alloc hybrid program.c
    python3 MiniCC.py --help

Exit codes:
    0  success
    1  runtime error (eval mode)
    2  type error
    3  syntax error
    4  internal compiler error
    5  unsupported feature
"""

from __future__ import annotations

from argparse import ArgumentParser
from traceback import print_exc
import os
import sys

import antlr4
from antlr4.error.ErrorListener import ErrorListener

from MiniCLexer import MiniCLexer
from MiniCParser import MiniCParser
from TypingAndInterpret.MiniCTypingVisitor import MiniCTypingVisitor, MiniCTypeError
from TypingAndInterpret.MiniCInterpretVisitor import MiniCInterpretVisitor
from Lib.Errors import (MiniCUnsupportedError, MiniCInternalError,
                        MiniCRuntimeError, AllocationError)


MODES = ['parse', 'typecheck', 'eval', 'codegen-linear']
REG_ALLOCS = ['none', 'naive', 'all-in-mem', 'hybrid']


class CountErrorListener(ErrorListener):
    """Count lexer and parser errors (the ANTLR lexer has no built-in counter)."""

    def __init__(self):
        super().__init__()
        self.count = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.count += 1


def parse(inputname):
    input_s = antlr4.FileStream(inputname, encoding='utf-8')
    lexer = MiniCLexer(input_s)
    counter = CountErrorListener()
    lexer._listeners.append(counter)
    parser = MiniCParser(antlr4.CommonTokenStream(lexer))
    parser._listeners.append(counter)
    tree = parser.prog()
    if counter.count > 0:
        exit(3)
    return parser, tree


def make_allocator(reg_alloc, fdata):
    """Return (allocator, comment) for the chosen allocation strategy."""
    if reg_alloc == "naive":
        from Lib.Allocator import NaiveAllocator
        return NaiveAllocator(fdata), "naive allocation"
    if reg_alloc == "all-in-mem":
        from CodeGen.AllInMemAllocator import AllInMemAllocator
        return AllInMemAllocator(fdata), "all-in-memory allocation"
    if reg_alloc == "hybrid":
        from CodeGen.HybridNaiveAllocator import HybridNaiveAllocator
        return HybridNaiveAllocator(fdata), "hybrid allocation"
    if reg_alloc == "none":
        return None, "non executable 3-address code"
    raise ValueError("Invalid allocation strategy: " + reg_alloc)


def main(inputname, mode, reg_alloc=None, typecheck=True,
         stdout=False, output_name=None, debug=False):
    parser, tree = parse(inputname)

    if typecheck and mode != 'parse':
        try:
            MiniCTypingVisitor().visit(tree)
        except MiniCTypeError as e:
            print(e.args[0])
            exit(2)

    if mode == 'eval':
        try:
            MiniCInterpretVisitor().visit(tree)
        except MiniCRuntimeError as e:
            print(e.args[0])
            exit(1)
        except MiniCInternalError as e:
            print(e.args[0], file=sys.stderr)
            exit(4)
        return

    if mode != 'codegen-linear':
        return

    if stdout:
        output_name = None
    elif output_name is None:
        output_name = os.path.splitext(inputname)[0] + ".s"
        print("Code will be generated in file " + output_name)

    from CodeGen.MiniCCodeGen3AVisitor import MiniCCodeGen3AVisitor
    codegen = MiniCCodeGen3AVisitor(debug, parser)

    with open(output_name, 'w') if output_name else sys.stdout as output:
        codegen.visit(tree)
        for code in codegen.get_functions():
            allocator, comment = make_allocator(reg_alloc, code.fdata)
            if allocator:
                allocator.prepare()
                allocator.rewriteCode(code)
            output.write(f"# Options: {' '.join(sys.argv[1:])}\n")
            code.print_code(output, comment=comment)
            if debug:
                codegen.printSymbolTable()


if __name__ == '__main__':
    argparser = ArgumentParser(description='MiniC compiler (subset of C to RISC-V)')
    argparser.add_argument('filename', type=str, help='Source file.')
    argparser.add_argument('--mode', type=str, choices=MODES, required=True,
                           help='What to do with the input program')
    argparser.add_argument('--reg-alloc', type=str, choices=REG_ALLOCS,
                           help='Register allocation (codegen-linear only)')
    argparser.add_argument('--stdout', action='store_true',
                           help='Print the generated code on standard output')
    argparser.add_argument('--output', type=str,
                           help='Output file for the generated code')
    argparser.add_argument('--disable-typecheck', action='store_true',
                           help="Skip the typechecker")
    argparser.add_argument('--debug', action='store_true',
                           help='Print debug information')
    args = argparser.parse_args()

    if args.mode == 'codegen-linear' and args.reg_alloc is None:
        print("error: --reg-alloc is required with --mode codegen-linear")
        exit(1)
    if args.mode != 'codegen-linear' and args.reg_alloc is not None:
        print("error: --reg-alloc is only valid with --mode codegen-linear")
        exit(1)

    try:
        main(args.filename, args.mode, args.reg_alloc,
             not args.disable_typecheck, args.stdout, args.output, args.debug)
    except MiniCUnsupportedError as e:
        print(e)
        exit(5)
    except (MiniCInternalError, AllocationError):
        print_exc()
        exit(4)
