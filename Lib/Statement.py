"""
The base class for RISCV ASM statements is :py:class:`Statement`.
It is inherited by :py:class:`Comment`, :py:class:`Label`
and :py:class:`Instruction`. In turn, :py:class:`Instruction`
is inherited by :py:class:`Instru3A`
(for regular non-branching 3-address instructions),
:py:class:`AbsoluteJump` and :py:class:`ConditionalJump`.
"""

from dataclasses import dataclass
from typing import (List, Dict, TypeVar)
from Lib.Operands import (Operand, Renamer, Temporary, RegisterLike, Condition)
from Lib.Errors import MiniCInternalError


def regset_to_string(registerset) -> str:
    """Utility function: pretty-prints a set of locations."""
    return "{" + ",".join(str(x) for x in registerset) + "}"


# Temporary until we can use Typing.Self in python 3.11
TStatement = TypeVar("TStatement", bound="Statement")


@dataclass(unsafe_hash=True)
class Statement:
    """A Statement, which is an instruction, a comment or a label."""

    def defined(self) -> List[Operand]:
        """Operands defined (written) in this instruction"""
        return []

    def used(self) -> List[Operand]:
        """Operands used (read) in this instruction"""
        return []

    def substitute(self: TStatement, subst: Dict[Operand, Operand]) -> TStatement:
        """Return a new instruction, cloned from this one, replacing operands
        that appear as key in subst by their value."""
        raise Exception(
            f"substitute: Operands {subst} are not present in instruction {self}")

    def with_args(self: TStatement, new_args: List[Operand]) -> TStatement:
        """Return a new instruction, cloned from this one, where operands have
        been replaced by new_args."""
        raise Exception(
                f"substitute: Operands {new_args} are not present in instruction {self}")

    def printIns(self, stream):
        """
        Print the statement on the given output.
        Should never be called on the base class.
        """
        raise NotImplementedError


@dataclass(unsafe_hash=True)
class Comment(Statement):
    """A comment."""
    comment: str

    def __str__(self):  # use only for print_dot !
        return f"# {self.comment}"

    def printIns(self, stream):
        print('        # ' + self.comment, file=stream)


@dataclass(unsafe_hash=True)
class Label(Statement, Operand):
    """A label is both a Statement and an Operand."""
    name: str

    def __str__(self):
        return (f"lbl_{self.name}")

    def __repr__(self):
        return (f"{self.name}")

    def printIns(self, stream):
        print(str(self) + ':', file=stream)


@dataclass(init=False)
class Instruction(Statement):
    ins: str
    _read_only: bool

    def is_read_only(self):
        """
        True if the instruction only reads from its operands.

        Otherwise, the first operand is considered as the destination
        and others are source.
        """
        return self._read_only

    def rename(self, renamer: Renamer) -> None:
        raise NotImplementedError

    def args(self) -> List[Operand]:
        """List of operands the instruction takes"""
        raise NotImplementedError

    def defined(self):
        if self.is_read_only():
            defs = []
        else:
            defs = [self.args()[0]]
        return defs

    def used(self) -> List[Operand]:
        if self.is_read_only():
            uses = self.args()
        else:
            uses = self.args()[1:]
        return uses

    def __str__(self):
        s = self.ins
        first = True
        for arg in self.args():
            if first:
                s += ' ' + str(arg)
                first = False
            else:
                s += ', ' + str(arg)
        return s

    def __hash__(self):
        return hash((self.ins, *self.args()))

    def printIns(self, stream):
        """Print the instruction on the given output."""
        print('       ', str(self), file=stream)


@dataclass(init=False)
class Instru3A(Instruction):
    _args: List[Operand]

    def __init__(self, ins, *args: Operand):
        # convention is to use lower-case in RISCV
        self.ins = ins.lower()
        self._args = list(args)
        self._read_only = (self.ins == "call"
                           or self.ins == "ld"
                           or self.ins == "lw"
                           or self.ins == "lb")
        if (self.ins.startswith("b") or self.ins == "j"):
            raise MiniCInternalError

    def args(self):
        return self._args

    def rename(self, renamer: Renamer):
        old_replaced = dict()
        for i, arg in enumerate(self._args):
            if isinstance(arg, Temporary):
                if i == 0 and not self.is_read_only():
                    old_replaced[arg] = renamer.replace(arg)
                    new_t = renamer.fresh(arg)
                elif arg in old_replaced.keys():
                    new_t = old_replaced[arg]
                else:
                    new_t = renamer.replace(arg)
                self._args[i] = new_t

    def substitute(self, subst: Dict[Operand, Operand]):
        for op in subst:
            if op not in self.args():
                raise Exception(
                    f"substitute: Operand {op} is not present in instruction {self}")
        args = [subst.get(arg, arg)
                if isinstance(arg, Temporary) else arg
                for arg in self.args()]
        return Instru3A(self.ins, *args)

    def with_args(self, new_args: List[Operand]):
        if len(new_args) != len(self._args):
            raise Exception(
                f"substitute: Expected {len(self._args)} operands for {self}, got {new_args}.")
        return Instru3A(self.ins, *new_args)

    def __hash__(self):
        return hash(super)


@dataclass(init=False)
class AbsoluteJump(Instruction):
    """ An Absolute Jump is a specific kind of instruction"""
    ins = "j"
    label: Label
    _read_only = True

    def __init__(self, label: Label):
        self.label = label

    def args(self) -> List[Operand]:
        return [self.label]

    def rename(self, renamer: Renamer):
        pass

    def substitute(self, subst: Dict[Operand, Operand]):
        if subst != {}:
            raise Exception(
                f"substitute: No possible substitution on instruction {self}")
        return self

    def with_args(self, new_args: List[Operand]):
        if new_args != self.args():
            raise Exception(
                f"substitute: No possible substitution on instruction {self}. "
                f"Old args={self.args()}, new args={new_args}")
        return self

    def __hash__(self):
        return hash(super)

    def targets(self) -> List[Label]:
        """Return the labels targetted by the AbsoluteJump."""
        return [self.label]


@dataclass(init=False)
class ConditionalJump(Instruction):
    """ A Conditional Jump is a specific kind of instruction"""
    cond: Condition
    label: Label
    op1: RegisterLike
    op2: RegisterLike
    _read_only = True

    def __init__(self, cond: Condition, op1: RegisterLike, op2: RegisterLike, label: Label):
        self.cond = cond
        self.label = label
        self.op1 = op1
        self.op2 = op2
        self.ins = str(self.cond)

    def args(self):
        return [self.op1, self.op2, self.label]

    def rename(self, renamer: Renamer):
        if isinstance(self.op1, Temporary):
            self.op1 = renamer.replace(self.op1)
        if isinstance(self.op2, Temporary):
            self.op2 = renamer.replace(self.op2)

    def substitute(self, subst: Dict[Operand, Operand]):
        for op in subst:
            if op not in self.args():
                raise Exception(
                    f"substitute: Operand {op} is not present in instruction {self}")
        op1 = subst.get(self.op1, self.op1) if isinstance(self.op1, Temporary) \
            else self.op1
        op2 = subst.get(self.op2, self.op2) if isinstance(self.op2, Temporary) \
            else self.op2
        assert isinstance(op1, RegisterLike)
        assert isinstance(op2, RegisterLike)
        return ConditionalJump(self.cond, op1, op2, self.label)

    def with_args(self, new_args: List[Operand]):
        if len(new_args) != 3:
            raise Exception(
                f"substitute: Expected 3 operands for {self}, got {new_args}.")
        assert isinstance(new_args[2], Label)
        label: Label = new_args[2]
        assert isinstance(new_args[0], RegisterLike)
        assert isinstance(new_args[1], RegisterLike)
        return ConditionalJump(self.cond, new_args[0], new_args[1], label)

    def __hash__(self):
        return hash(super)
