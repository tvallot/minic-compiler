from Lib.Operands import GP_REGS, DataLocation, Temporary
from CodeGen.AllInMemAllocator import AllInMemAllocator
from typing import Dict


class HybridNaiveAllocator(AllInMemAllocator):
    """Put temporaries in registers while there are free ones,
    then on the stack.

    The rewriting of instructions is the same as AllInMemAllocator:
    only temporaries stored in memory need loads and stores.
    """

    def prepare(self) -> None:
        regs = list(GP_REGS)  # writable copy
        temp_allocation: Dict[Temporary, DataLocation] = dict()
        for tmp in self._fdata._pool.get_all_temps():
            if regs:
                temp_allocation[tmp] = regs.pop()
            else:
                temp_allocation[tmp] = self._fdata.fresh_offset()
        self._fdata._pool.set_temp_allocation(temp_allocation)
