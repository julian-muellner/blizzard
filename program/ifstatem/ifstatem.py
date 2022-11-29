from program.condition import Condition
from utils import indent_string


class IfStatem:
    condition: Condition
    if_branch = None
    else_branch = None
    pc: int

    def __init__(self, condition, if_branch, else_branch=None):
        self.else_branch = else_branch
        self.condition = condition
        self.if_branch = if_branch
        self.pc = -1
        self.next_stmt = None

    def assign_pc(self, pc) -> int:
        self.pc = pc
        pc = pc + 1

        for stmt in self.if_branch:
            pc = stmt.assign_pc(pc)
        if self.else_branch:
            for stmt in self.else_branch:
                pc = stmt.assign_pc(pc)
        return pc

    def assign_next_stmt(self, next_stmt):
        self.next_stmt = next_stmt

        block_length = len(self.if_branch)
        for i in range(block_length - 1):
            stmt = self.if_branch[i] 
            stmt.assign_next_stmt(self.if_branch[i + 1])
        self.if_branch[block_length - 1].assign_next_stmt(next_stmt)

        if self.else_branch is None:
            return

        block_length = len(self.else_branch)
        # next_stmt of last statement remains None, parent stays set to None
        for i in range(block_length - 1):
            stmt = self.else_branch[i] 
            stmt.assign_next_stmt(self.else_branch[i + 1])
        self.else_branch[block_length - 1].assign_next_stmt(next_stmt)

    def __str__(self):
        def branch_to_str(branch):
            return indent_string("\n".join([str(b) for b in branch]), 4)

        string = f"{self.pc}: if {self.condition}:\n{branch_to_str(self.if_branch)}"
        if self.else_branch:
            string += f"\nelse:\n{branch_to_str(self.else_branch)}"

        return string
