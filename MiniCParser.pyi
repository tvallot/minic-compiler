from antlr4.error.ErrorListener import ErrorListener
from antlr4.Parser import Parser
from typing import Callable, Any, List

class MiniCParser(Parser):
    _listeners: List[ErrorListener]
    prog: Callable[[], Any]
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
    NEQ: int
    INTTYPE: int
    FLOATTYPE: int
    BOOLTYPE: int
    STRINGTYPE: int
