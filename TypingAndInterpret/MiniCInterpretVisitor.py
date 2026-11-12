# Visitor to *interpret* MiniC files
from typing import (
  Dict,
  List)
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.Errors import MiniCRuntimeError, MiniCInternalError, MiniCUnsupportedError

MINIC_VALUE = int | str | bool | float | List['MINIC_VALUE']


class ContinueException(Exception):
    """Raised by `continue` and caught by the enclosing loop."""
    pass


class MiniCInterpretVisitor(MiniCVisitor):

    _memory: Dict[str, MINIC_VALUE]

    def __init__(self):
        self._memory = dict()  # store all variable ids and values.
        self.has_main = False

    # visitors for variable declarations

    def visitVarDecl(self, ctx) -> None:
        # Initialise all variables in self._memory
        type_str = ctx.typee().getText()
        match type_str:
            case "int":
                init_value = 0
            case "float":
                init_value = 0.0
            case "bool":
                init_value = False
            case "string":
                init_value = ""
            case _:
                raise MiniCInternalError(f"Initialization for type {type_str}")

        names = self.visit(ctx.id_l())

        for name in names:
            self._memory[name] = init_value

    def visitIdList(self, ctx) -> List[str]:
        head = ctx.ID().getText()
        tail = self.visit(ctx.id_l())
        return [head] + tail

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # visitors for atoms --> value

    def visitParExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> int:
        return int(ctx.getText())

    def visitFloatAtom(self, ctx) -> float:
        return float(ctx.getText())

    def visitBooleanAtom(self, ctx) -> bool:
        return ctx.getText() == "true"

    def visitIdAtom(self, ctx) -> MINIC_VALUE:
        name = ctx.ID().getText()
        if name not in self._memory:
            raise MiniCInternalError(f"Undefined variable {name}")
        return self._memory[name]

    def visitStringAtom(self, ctx) -> str:
        return ctx.getText()[1:-1]  # Remove the ""

    # visit expressions

    def visitAtomExpr(self, ctx) -> MINIC_VALUE:
        return self.visit(ctx.atom())

    # || and && are lazy, like in C: the right operand is only
    # evaluated when needed.
    def visitOrExpr(self, ctx) -> bool:
        return self.visit(ctx.expr(0)) or self.visit(ctx.expr(1))

    def visitAndExpr(self, ctx) -> bool:
        return self.visit(ctx.expr(0)) and self.visit(ctx.expr(1))

    def visitEqualityExpr(self, ctx) -> bool:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        # be careful for float equality
        if ctx.myop.type == MiniCParser.EQ:
            return lval == rval
        else:
            return lval != rval

    def visitRelationalExpr(self, ctx) -> bool:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.LT:
            return lval < rval
        elif ctx.myop.type == MiniCParser.LTEQ:
            return lval <= rval
        elif ctx.myop.type == MiniCParser.GT:
            return lval > rval
        elif ctx.myop.type == MiniCParser.GTEQ:
            return lval >= rval
        else:
            raise MiniCInternalError(
                f"Unknown comparison operator '{ctx.myop}'"
            )

    def visitAdditiveExpr(self, ctx) -> MINIC_VALUE:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        if ctx.myop.type == MiniCParser.PLUS:
            if isinstance(lval, str) or isinstance(rval, str):
                return f'{lval}{rval}'
            else:
                return lval + rval
        elif ctx.myop.type == MiniCParser.MINUS:
            return lval - rval
        else:
            raise MiniCInternalError(
                f"Unknown additive operator '{ctx.myop}'")

    def visitMultiplicativeExpr(self, ctx) -> MINIC_VALUE:
        assert ctx.myop is not None
        lval = self.visit(ctx.expr(0))
        rval = self.visit(ctx.expr(1))
        match ctx.myop.type:
            case MiniCParser.MULT:
                return lval * rval

            case MiniCParser.DIV:
                if rval == 0:
                    raise MiniCRuntimeError("Division by 0")
                if isinstance(lval, int) and isinstance(rval, int):
                    # C rounds toward zero, Python's // rounds down
                    return int(lval / rval)
                return lval / rval

            case MiniCParser.MOD:
                if rval == 0:
                    raise MiniCRuntimeError("Division by 0")
                # Same sign rule as C: a % b == a - (a / b) * b
                quotient = int(lval / rval)
                return lval - quotient * rval

            case _: raise MiniCInternalError(
                    f"Unknown multiplicative operator '{ctx.myop}'")

    def visitNotExpr(self, ctx) -> bool:
        return not self.visit(ctx.expr())

    def visitUnaryMinusExpr(self, ctx) -> MINIC_VALUE:
        return -self.visit(ctx.expr())

    # visit statements

    def visitPrintlnintStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        assert isinstance(val, int)
        print(val)

    def visitPrintlnfloatStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        assert isinstance(val, float)
        print(f"{val:.2f}")

    def visitPrintlnboolStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        assert isinstance(val, bool)
        print('1' if val else '0')

    def visitPrintlnstringStat(self, ctx) -> None:
        val = self.visit(ctx.expr())
        assert isinstance(val, str)
        print(val)

    def visitAssignStat(self, ctx) -> None:
        name = ctx.ID().getText()
        if name not in self._memory:
            raise MiniCInternalError(f"Undefined variable {name}")
        value = self.visit(ctx.expr())
        self._memory[name] = value

    def visitIfStat(self, ctx) -> None:
        if self.visit(ctx.expr()):
            self.visit(ctx.then_block)
        elif ctx.else_block is not None:
            self.visit(ctx.else_block)

    def visitWhileStat(self, ctx) -> None:
        while self.visit(ctx.expr()):
            try:
                self.visit(ctx.body)
            except ContinueException:
                pass

    def visitForStat(self, ctx) -> None:
        if ctx.init is not None:
            self.visit(ctx.init)
        while ctx.cond is None or self.visit(ctx.cond):
            try:
                self.visit(ctx.body)
            except ContinueException:
                pass
            if ctx.update is not None:
                self.visit(ctx.update)

    def visitContinueStat(self, ctx) -> None:
        raise ContinueException()

    # TOPLEVEL
    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)
        if not self.has_main:
            # A program without a main function is compilable (hence
            # it's not a typing error per se), but not executable,
            # hence we consider it a runtime error.
            raise MiniCRuntimeError("No main function in file")

    # Visit a function: ignore if non main!
    def visitFuncDef(self, ctx) -> None:
        funname = ctx.ID().getText()
        if funname == "main":
            self.has_main = True
            self.visit(ctx.vardecl_l())
            self.visit(ctx.block())
        else:
            raise MiniCUnsupportedError("Functions are not supported in evaluation mode")
