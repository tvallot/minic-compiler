from typing import Callable, List
from MiniCVisitor import MiniCVisitor
from MiniCParser import MiniCParser
from Lib.LinearCode import CodeStatement, LinearCode
from Lib import RiscV
from Lib.RiscV import Condition
from Lib import Operands
from antlr4.tree.Trees import Trees
from Lib.Errors import MiniCInternalError, MiniCUnsupportedError

"""
Three-address code generation for MiniC.
This visitor constructs an object of type "LinearCode".
"""


class MiniCCodeGen3AVisitor(MiniCVisitor):

    _current_function: LinearCode
    # Shortcuts for methods of member objects
    fresh_tmp: Callable[[], Operands.Temporary]
    fresh_label: Callable[[str], RiscV.Label]
    add_statement: Callable[[CodeStatement], None]
    add_instruction_PRINTLN_INT: Callable[[Operands.DataLocation], None]
    add_comment: Callable[[str], None]
    get_label_div_by_zero: Callable[[], RiscV.Label]
    _symbol_table: dict[str, Operands.Temporary]

    def __init__(self, debug, parser):
        super().__init__()
        self._parser = parser
        self._debug = debug
        self._functions = []
        self._lastlabel = ""
        self._continue_labels: List[RiscV.Label] = []  # innermost loop last

    def get_functions(self) -> List[LinearCode]:
        return self._functions

    def printSymbolTable(self):  # pragma: no cover
        print("--variables to temporaries map--")
        for keys, values in self._symbol_table.items():
            print(keys + '-->' + str(values))

    # handle variable decl

    def visitVarDecl(self, ctx) -> None:
        type_str = ctx.typee().getText()
        vars_l = self.visit(ctx.id_l())
        for name in vars_l:
            if name in self._symbol_table:
                raise MiniCInternalError(
                    f"Variable {name} has already been declared")
            else:
                tmp = self.fresh_tmp()
                self._symbol_table[name] = tmp
                if type_str not in ("int", "bool"):
                    raise MiniCUnsupportedError(f"Unsupported type {type_str}")
                # Initialization to 0 or False, both represented with 0
                self.add_statement(
                    RiscV.li(tmp, Operands.Immediate(0)))

    def visitIdList(self, ctx) -> List[str]:
        t = self.visit(ctx.id_l())
        t.append(ctx.ID().getText())
        return t

    def visitIdListBase(self, ctx) -> List[str]:
        return [ctx.ID().getText()]

    # expressions

    def visitParExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.expr())

    def visitIntAtom(self, ctx) -> Operands.Temporary:
        val = Operands.Immediate(int(ctx.getText()))
        dest_temp = self.fresh_tmp()
        self.add_statement(RiscV.li(dest_temp, val))
        return dest_temp

    def visitFloatAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("float literal")

    def visitBooleanAtom(self, ctx) -> Operands.Temporary:
        # true is 1, false is 0
        value = 1 if ctx.getText() == "true" else 0
        dest_temp = self.fresh_tmp()
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(value)))
        return dest_temp

    def visitIdAtom(self, ctx) -> Operands.Temporary:
        try:
            # get the temporary associated to id
            return self._symbol_table[ctx.getText()]
        except KeyError:  # pragma: no cover
            raise MiniCInternalError(
                f"Undefined variable {ctx.getText()}, this should have failed to typecheck."
            )

    def visitStringAtom(self, ctx) -> Operands.Temporary:
        raise MiniCUnsupportedError("string atom")

    # expressions

    def visitAtomExpr(self, ctx) -> Operands.Temporary:
        return self.visit(ctx.atom())

    def visitAdditiveExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        dest_temp = self.fresh_tmp()
        if ctx.myop.type == MiniCParser.PLUS:
            self.add_statement(RiscV.add(dest_temp, left, right))
        elif ctx.myop.type == MiniCParser.MINUS:
            self.add_statement(RiscV.sub(dest_temp, left, right))
        else:  # pragma: no cover
            raise MiniCInternalError(f"Unknown additive operator: {ctx.myop.text}")
        return dest_temp

    def _jump_if_zero(self, label: RiscV.Label, value: Operands.Temporary) -> None:
        self.add_statement(RiscV.conditional_jump(
            label, value, Condition(MiniCParser.EQ), Operands.ZERO))

    def _jump_if_not_zero(self, label: RiscV.Label, value: Operands.Temporary) -> None:
        self.add_statement(RiscV.conditional_jump(
            label, value, Condition(MiniCParser.NEQ), Operands.ZERO))

    def visitOrExpr(self, ctx) -> Operands.Temporary:
        # Lazy evaluation, like in C: if the left side is true,
        # the right side is not evaluated.
        #     dest = 1
        #     if left != 0 goto end
        #     if right != 0 goto end
        #     dest = 0
        #   end:
        dest_temp = self.fresh_tmp()
        end_label = self.fresh_label("or_end")
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(1)))
        self._jump_if_not_zero(end_label, self.visit(ctx.expr(0)))
        self._jump_if_not_zero(end_label, self.visit(ctx.expr(1)))
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(0)))
        self.add_statement(end_label)
        return dest_temp

    def visitAndExpr(self, ctx) -> Operands.Temporary:
        # Lazy evaluation, like in C: if the left side is false,
        # the right side is not evaluated.
        #     dest = 0
        #     if left == 0 goto end
        #     if right == 0 goto end
        #     dest = 1
        #   end:
        dest_temp = self.fresh_tmp()
        end_label = self.fresh_label("and_end")
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(0)))
        self._jump_if_zero(end_label, self.visit(ctx.expr(0)))
        self._jump_if_zero(end_label, self.visit(ctx.expr(1)))
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(1)))
        self.add_statement(end_label)
        return dest_temp

    def visitEqualityExpr(self, ctx) -> Operands.Temporary:
        return self.visitRelationalExpr(ctx)

    def visitRelationalExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None
        c = Condition(ctx.myop.type)
        if self._debug:
            print("relational expression:")
            print(Trees.toStringTree(ctx, [], self._parser))
            print("Condition:", c)
        #     dest = 0
        #     if !(left op right) goto end
        #     dest = 1
        #   end:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        dest_temp = self.fresh_tmp()
        end_label = self.fresh_label("end_relational")
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(0)))
        self.add_statement(RiscV.conditional_jump(end_label, left, c.negate(), right))
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(1)))
        self.add_statement(end_label)
        return dest_temp

    def visitMultiplicativeExpr(self, ctx) -> Operands.Temporary:
        assert ctx.myop is not None
        div_by_zero_lbl = self.get_label_div_by_zero()
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        dest_temp = self.fresh_tmp()
        match ctx.myop.type:
            case MiniCParser.MULT:
                self.add_statement(RiscV.mul(dest_temp, left, right))
            case MiniCParser.DIV:
                self._jump_if_zero(div_by_zero_lbl, right)
                self.add_statement(RiscV.div(dest_temp, left, right))
            case MiniCParser.MOD:
                self._jump_if_zero(div_by_zero_lbl, right)
                self.add_statement(RiscV.rem(dest_temp, left, right))
            case _:  # pragma: no cover
                raise MiniCInternalError(
                    f"Unknown multiplicative operator '{ctx.myop}'")
        return dest_temp

    def visitNotExpr(self, ctx) -> Operands.Temporary:
        #     dest = 1
        #     if expr == 0 goto end
        #     dest = 0
        #   end:
        expr_temp = self.visit(ctx.expr())
        dest_temp = self.fresh_tmp()
        end_label = self.fresh_label("not_end")
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(1)))
        self._jump_if_zero(end_label, expr_temp)
        self.add_statement(RiscV.li(dest_temp, Operands.Immediate(0)))
        self.add_statement(end_label)
        return dest_temp

    def visitUnaryMinusExpr(self, ctx) -> Operands.Temporary:
        expr_temp = self.visit(ctx.expr())
        dest_temp = self.fresh_tmp()
        self.add_statement(RiscV.sub(dest_temp, Operands.ZERO, expr_temp))
        return dest_temp

    def visitProgRule(self, ctx) -> None:
        self.visitChildren(ctx)

    def visitFuncDef(self, ctx) -> None:
        funcname = ctx.ID().getText()
        self._current_function = LinearCode(funcname)

        # Our code can deal with multiple functions, and each function is a
        # different LinearCode object. But don't bother the user with
        # self._current_function each time, define a few shortcuts to make the
        # code simpler. This comes here and not in __init__ since we need
        # _current_fuction to be set, and need to redefine the shortcut when
        # _current_function changes.
        self.fresh_tmp = self._current_function.fdata.fresh_tmp
        self.fresh_label = self._current_function.fdata.fresh_label
        self.add_statement = self._current_function.add_statement
        self.add_instruction_PRINTLN_INT = self._current_function.add_instruction_PRINTLN_INT
        self.add_comment = self._current_function.add_comment
        self.get_label_div_by_zero = self._current_function.fdata.get_label_div_by_zero

        self._symbol_table = dict()

        self.add_comment("Variable declarations:")
        self.visit(ctx.vardecl_l())
        self.add_comment("Function body:")
        self.visit(ctx.block())
        self.add_comment("Return at end of function:")
        # This skeleton doesn't deal properly with functions, and
        # hardcodes a "return 0;" at the end of function. Generate
        # code for this "return 0;".
        self.add_statement(
            RiscV.li(Operands.A0, Operands.Immediate(0)))
        self._functions.append(self._current_function)
        del self._current_function

    def visitAssignStat(self, ctx) -> None:
        if self._debug:
            print("assign statement, rightexpression is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
        expr_temp = self.visit(ctx.expr())
        name = ctx.ID().getText()
        self.add_statement(RiscV.mv(self._symbol_table[name], expr_temp))

    def visitIfStat(self, ctx) -> None:
        if self._debug:
            print("if statement")
        #     if cond == 0 goto else
        #     <then block>
        #     goto end_if
        #   else:
        #     <else block>
        #   end_if:
        end_if_label = self.fresh_label("end_if")
        cond_temp = self.visit(ctx.expr())
        if ctx.else_block is None:
            self._jump_if_zero(end_if_label, cond_temp)
            self.visit(ctx.then_block)
        else:
            else_label = self.fresh_label("else")
            self._jump_if_zero(else_label, cond_temp)
            self.visit(ctx.then_block)
            self.add_statement(RiscV.jump(end_if_label))
            self.add_statement(else_label)
            self.visit(ctx.else_block)
        self.add_statement(end_if_label)

    def visitWhileStat(self, ctx) -> None:
        if self._debug:
            print("while statement, condition is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
            print("and block is:")
            print(Trees.toStringTree(ctx.stat_block(), [], self._parser))
        #   begin:
        #     if cond == 0 goto end
        #     <body>            (continue jumps to begin)
        #     goto begin
        #   end:
        begin_label = self.fresh_label("begin_while")
        end_label = self.fresh_label("end_while")
        self.add_statement(begin_label)
        self._jump_if_zero(end_label, self.visit(ctx.expr()))
        self._continue_labels.append(begin_label)
        self.visit(ctx.body)
        self._continue_labels.pop()
        self.add_statement(RiscV.jump(begin_label))
        self.add_statement(end_label)

    def visitForStat(self, ctx) -> None:
        if self._debug:
            print("for statement")
            print(Trees.toStringTree(ctx, [], self._parser))
        #     <init>
        #   begin:
        #     if cond == 0 goto end     (no test if cond is empty)
        #     <body>                    (continue jumps to update)
        #   update:
        #     <update>
        #     goto begin
        #   end:
        begin_label = self.fresh_label("begin_for")
        update_label = self.fresh_label("update_for")
        end_label = self.fresh_label("end_for")
        if ctx.init is not None:
            self.visit(ctx.init)
        self.add_statement(begin_label)
        if ctx.cond is not None:
            self._jump_if_zero(end_label, self.visit(ctx.cond))
        self._continue_labels.append(update_label)
        self.visit(ctx.body)
        self._continue_labels.pop()
        self.add_statement(update_label)
        if ctx.update is not None:
            self.visit(ctx.update)
        self.add_statement(RiscV.jump(begin_label))
        self.add_statement(end_label)

    def visitContinueStat(self, ctx) -> None:
        # The typechecker already rejects `continue` outside of a loop.
        self.add_statement(RiscV.jump(self._continue_labels[-1]))

    # visit statements

    def visitPrintlnintStat(self, ctx) -> None:
        expr_loc = self.visit(ctx.expr())
        if self._debug:
            print("print_int statement, expression is:")
            print(Trees.toStringTree(ctx.expr(), [], self._parser))
        self.add_instruction_PRINTLN_INT(expr_loc)

    def visitPrintlnboolStat(self, ctx) -> None:
        expr_loc = self.visit(ctx.expr())
        self.add_instruction_PRINTLN_INT(expr_loc)

    def visitPrintlnfloatStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type float")

    def visitPrintlnstringStat(self, ctx) -> None:
        raise MiniCUnsupportedError("Unsupported type string")

    def visitStatList(self, ctx) -> None:
        for stat in ctx.stat():
            self.add_comment(Trees.toStringTree(stat, [], self._parser))
            self.visit(stat)
