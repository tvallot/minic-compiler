from antlr4 import ParseTreeVisitor
from typing import Any, Callable, Concatenate

# Minimalist stub needed from Pyright 1.1.408, or it considers that the return
# value of visit is None and raise pages of errors.
class MiniCVisitor(ParseTreeVisitor):
    visit: Callable[Concatenate[int, ...], Any]
