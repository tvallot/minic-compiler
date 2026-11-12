# MiniC compiler
#
#   make                 generate the parser from MiniC.g4
#   make test            run all tests (interpreter + code generation)
#   make test-interpret  typechecker and interpreter tests
#   make test-codegen    code generation tests (all allocators)
#   make run FILE=examples/gcd.c [ALLOC=hybrid]
#                        compile a program and run it in the RISC-V simulator
#   make clean           remove generated files
#
# Run a subset of tests:  make test FILTER='CodeGen/tests/custom/**/*for*.c'
# Stop at the first failure:  make test PYTEST_OPTS=-x

# Use the `antlr4` command if it exists, else the jar from the Docker image
ANTLR_JAR ?= /opt/antlr-4.13.2-complete.jar
ANTLR4 ?= $(if $(shell command -v antlr4),antlr4,java -jar $(ANTLR_JAR))
ALLOC ?= hybrid
PYTEST_OPTS ?=
PYTEST = python3 -m pytest -v -rs --failed-first -n auto $(PYTEST_OPTS)

ifdef FILTER
export FILTER
endif

all: antlr

antlr: MiniCLexer.py MiniCParser.py

MiniCLexer.py MiniCParser.py: MiniC.g4
	$(ANTLR4) $< -Dlanguage=Python3 -visitor -no-listener -Werror

test: test-interpret test-codegen

test-interpret: antlr
	$(PYTEST) test_interpreter.py

test-codegen: antlr
	MINICC_OPTS="--mode codegen-linear" $(PYTEST) test_codegen.py

run: antlr
	python3 MiniCC.py --mode codegen-linear --reg-alloc $(ALLOC) --output /tmp/minicc-out.s $(FILE)
	riscv64-unknown-elf-gcc /tmp/minicc-out.s libprint.s -o /tmp/minicc-out.riscv
	spike -m100 pk /tmp/minicc-out.riscv

typecheck: antlr
	pyright .

install-deps:
	python3 -m pip install antlr4-python3-runtime==4.13.2 pytest pytest-xdist

clean:
	find . \( -name "__pycache__" -o -name "*.riscv" -o -name "*.interp" -o -name "*.tokens" \) -print0 | xargs -0 rm -rf
	find . -path "*/tests/*" \( -name "*-naive.s" -o -name "*-gcc.s" -o -name "*-all-in-mem.s" -o -name "*-hybrid.s" \) -delete
	rm -f MiniCLexer.py MiniCParser.py MiniCVisitor.py

.PHONY: all antlr test test-interpret test-codegen run typecheck install-deps clean
.NOTPARALLEL:
