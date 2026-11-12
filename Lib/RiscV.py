"""
MIF08, CAP, CodeGeneration, RiscV API
Functions to define instructions.
"""

from Lib.Errors import MiniCInternalError
from Lib.Operands import (Condition, Immediate, Operand, RegisterLike, Function)
from Lib.Statement import (Instru3A, AbsoluteJump, ConditionalJump, Label)


def call(function: Function) -> Instru3A:
    """Function call."""
    return Instru3A('call', function)


def jump(label: Label) -> AbsoluteJump:
    """Unconditional jump to label."""
    return AbsoluteJump(label)


def conditional_jump(label: Label,
                     op1: RegisterLike,
                     cond: Condition,
                     op2: RegisterLike) -> ConditionalJump:
    """Add a conditional jump to the code.
    This is a wrapper around bge, bgt, beq, ... c is a Condition, like
    Condition('bgt'), Condition(MiniCParser.EQ), ...
    """
    return ConditionalJump(cond=cond, op1=op1, op2=op2, label=label)


def add(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    if isinstance(sr2orimm7, Immediate):
        return Instru3A("addi", dr, sr1, sr2orimm7)
    else:
        return Instru3A("add", dr, sr1, sr2orimm7)


def mul(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    if isinstance(sr2orimm7, Immediate):
        raise MiniCInternalError("Cant multiply by an immediate")
    else:
        return Instru3A("mul", dr, sr1, sr2orimm7)


def div(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    if isinstance(sr2orimm7, Immediate):
        raise MiniCInternalError("Cant divide by an immediate")
    else:
        return Instru3A("div", dr, sr1, sr2orimm7)


def rem(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    """REMainder, aka modulo (%)."""
    if isinstance(sr2orimm7, Immediate):
        raise MiniCInternalError("Cant divide by an immediate")
    return Instru3A("rem", dr, sr1, sr2orimm7)


def sub(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    if isinstance(sr2orimm7, Immediate):
        raise MiniCInternalError("Cant substract by an immediate")
    return Instru3A("sub", dr, sr1, sr2orimm7)


def land(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    """And instruction (cannot be called `and` due to Python and)."""
    return Instru3A("and", dr, sr1, sr2orimm7)


def lor(dr: RegisterLike, sr1: RegisterLike, sr2orimm7: RegisterLike | Immediate) -> Instru3A:
    """Or instruction (cannot be called `or` due to Python or)."""
    return Instru3A("or", dr, sr1, sr2orimm7)


def xor(dr: RegisterLike, sr1: RegisterLike,
        sr2orimm7: RegisterLike | Immediate) -> Instru3A:  # pragma: no cover
    if isinstance(sr2orimm7, Immediate):
        return Instru3A("xori", dr, sr1, sr2orimm7)
    else:
        return Instru3A("xor", dr, sr1, sr2orimm7)


def li(dr: RegisterLike, imm7: Immediate) -> Instru3A:
    return Instru3A("li", dr, imm7)


def mv(dr: Operand, sr: Operand) -> Instru3A:
    return Instru3A("mv", dr, sr)


def ld(dr: Operand, mem: Operand) -> Instru3A:
    return Instru3A("ld", dr, mem)


def sd(sr: Operand, mem: Operand) -> Instru3A:
    return Instru3A("sd", sr, mem)
