#! /usr/bin/env python3

import os
import sys
import pytest
import glob
from test_expect_pragma import (
    TestExpectPragmas, TestCompiler,
    cat
    )

"""
Tests for code generation (run with `make test-codegen`).

Each .c file in CodeGen/tests/ is compiled with each register allocator,
then run in the RISC-V simulator. The output is compared to the
`// EXPECTED` comments in the file. `test_expect` checks those comments
against GCC.
"""

MINICC_OPTS = []
if "MINICC_OPTS" in os.environ and os.environ["MINICC_OPTS"]:
    MINICC_OPTS = os.environ["MINICC_OPTS"].split()
else:
    MINICC_OPTS = ["--mode=codegen-linear"]

DISABLE_TYPECHECK = "--disable-typecheck" in MINICC_OPTS \
    or "--mode=parse" in MINICC_OPTS or "parse" in MINICC_OPTS
DISABLE_CODEGEN = "--mode=parse" in MINICC_OPTS or "--mode=typecheck" in MINICC_OPTS \
    or "parse" in MINICC_OPTS or "typecheck" in MINICC_OPTS

HERE = os.path.dirname(os.path.realpath(__file__))
if HERE == os.path.realpath('.'):
    HERE = '.'
TEST_DIR = HERE
IMPLEM_DIR = HERE
SKIP_EXPECT = False
if 'SKIP_EXPECT' in os.environ:
    SKIP_EXPECT = True

MINIC_COMPILE = os.path.join(IMPLEM_DIR, 'MiniCC.py')

ALL_FILES = []
# tests for typing AND evaluation
ALL_FILES += glob.glob(os.path.join(TEST_DIR, 'CodeGen/tests/**/[a-zA-Z]*.c'),
                       recursive=True)


SKIP_NOT_IMPLEMENTED = False
if 'SKIP_NOT_IMPLEMENTED' in os.environ:
    SKIP_NOT_IMPLEMENTED = True

if 'TEST_FILES' in os.environ:
    ALL_FILES = glob.glob(os.environ['TEST_FILES'], recursive=True)


ALL_IN_MEM_FILES = list(ALL_FILES)

if 'FILTER' in os.environ:
    abs_filter = os.path.join(HERE, os.environ['FILTER'])
    FILTER_FILES = glob.glob(abs_filter, recursive=True)
    print(f"Files filter (full path): {abs_filter} ({len(FILTER_FILES)} files found).")
    ALL_FILES = list(set(FILTER_FILES) & set(ALL_FILES))
    ALL_IN_MEM_FILES = list(set(FILTER_FILES) & set(ALL_IN_MEM_FILES))

# Avoid duplicates
ALL_IN_MEM_FILES.sort()
ALL_FILES = list(set(ALL_FILES))
ALL_FILES.sort()


class TestCodeGen(TestExpectPragmas, TestCompiler):
    DISABLE_CODEGEN = DISABLE_CODEGEN
    SKIP_NOT_IMPLEMENTED = SKIP_NOT_IMPLEMENTED
    MINIC_COMPILE = MINIC_COMPILE
    MINICC_OPTS = MINICC_OPTS

    # Not in test_expect_pragma to get assertion rewritting
    def assert_equal(self, actual, expected, compiler):
        if DISABLE_CODEGEN and expected.exitcode in (0, 5):
            # Compiler does not fail => no output expected
            assert actual.output == "", \
                "Compiler unexpectedly generated some output with codegen disabled"
            assert actual.exitcode == 0, \
                "Compiler unexpectedly failed with codegen disabled"
            return
        if DISABLE_TYPECHECK and expected.exitcode != 0:
            # Test should fail at typecheck, and we don't do
            # typechecking => nothing to check.
            pytest.skip("Test that doesn't typecheck with --disable-typecheck")
        assert actual.exitcode == expected.exitcode, \
            f"Exit code of the compiler ({compiler}) is incorrect"
        if expected.output is not None and actual.output is not None:
            assert actual.output == expected.output, \
                f"Output of the program is incorrect (using {compiler})."
        assert actual.execcode == expected.execcode, \
            f"Exit code of the execution is incorrect (after compiling with {compiler})"

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_expect(self, filename):
        """Test the EXPECTED annotations in test files by launching the
        program with GCC."""
        if SKIP_EXPECT:
            pytest.skip("Skipping all test_expect because $SKIP_EXPECT is set.")
        expect = self.get_expect(filename)
        if expect.skip_test_expected:
            pytest.skip("Skipping test_expect with GCC because "
                        "the test contains SKIP TEST EXPECTED")
        if expect.exitcode != 0:
            # GCC is more permissive than us, so trying to compile an
            # incorrect program would bring us no information (it may
            # compile, or fail with a different message...)
            pytest.skip("Not testing the expected value for tests expecting exitcode!=0")
        gcc_result = self.run_with_gcc(filename, expect)
        self.assert_equal(gcc_result, expect, "GCC")

    @pytest.mark.parametrize('filename', ALL_FILES)
    def test_naive_alloc(self, filename):
        cat(filename)  # For diagnosis
        expect = self.get_expect(filename)
        naive = self.compile_and_simulate(filename, expect, 'naive')
        self.assert_equal(naive, expect, "MiniCC with naive alloc")

    @pytest.mark.parametrize('filename', ALL_IN_MEM_FILES)
    def test_alloc_mem(self, filename):
        cat(filename)  # For diagnosis
        expect = self.get_expect(filename)
        actual = self.compile_and_simulate(filename, expect, 'all-in-mem')
        self.assert_equal(actual, expect, "MiniCC with all-in-mem")

    @pytest.mark.parametrize('filename', ALL_IN_MEM_FILES)
    def test_alloc_hybrid(self, filename):
        cat(filename)  # For diagnosis
        expect = self.get_expect(filename)
        actual = self.compile_and_simulate(filename, expect, 'hybrid')
        self.assert_equal(actual, expect, "MiniCC with hybrid alloc")



if __name__ == '__main__':
    pytest.main(sys.argv)
