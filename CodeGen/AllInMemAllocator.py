from Lib import RiscV
from Lib.Operands import Temporary, Operand, Offset, S
from Lib.Statement import Instruction
from Lib.Allocator import Allocator
from typing import List


class AllInMemAllocator(Allocator):
    """Store every temporary on the stack.

    Each instruction is rewritten to load its operands from memory into
    the scratch registers s1, s2, s3 before running, and to store its
    result back to memory after.
    """

    def replace(self, old_instr: Instruction) -> List[Instruction]:
        """Replace Temporary operands with their allocated location.

        Temporaries allocated to a register are used directly. Temporaries
        allocated in memory go through a scratch register.
        """
        scratch_regs = iter(S[1:4])
        before: List[Instruction] = []
        after: List[Instruction] = []
        new_args: List[Operand] = []

        for i, arg in enumerate(old_instr.args()):
            if not isinstance(arg, Temporary):
                new_args.append(arg)
                continue

            location = arg.get_alloced_loc()
            if not isinstance(location, Offset):
                # Already in a register
                new_args.append(location)
                continue

            reg = next(scratch_regs)
            # The first argument of an instruction that writes is its destination
            is_destination = i == 0 and not old_instr.is_read_only()
            if is_destination:
                after.append(RiscV.sd(reg, location))
            else:
                before.append(RiscV.ld(reg, location))
            new_args.append(reg)

        return before + [old_instr.with_args(new_args)] + after

    def prepare(self) -> None:
        """Allocate all temporaries to memory."""
        self._fdata._pool.set_temp_allocation(
            {temp: self._fdata.fresh_offset()
             for temp in self._fdata._pool.get_all_temps()})
