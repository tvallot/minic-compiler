from antlr4.error.ErrorListener import ErrorListener
from antlr4.Lexer import Lexer
from typing import Callable, Any, List

class MiniCLexer(Lexer):
    _listeners: List[ErrorListener]
    EQ: int
    LT: int
    LTEQ: int
    GT: int
    GTEQ: int
    PLUS: int
    MINUS: int
    MULT: int
    DIV: int
    MOD: int
