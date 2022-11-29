from program.condition import Condition
from utils import indent_string


class WhileStatem:
    condition: Condition
    body = None
    pc: int

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        self.pc = -1
        self.next_stmt = None

    def assign_pc(self, pc) -> int:
        self.pc = pc
        pc = pc + 1

        for stmt in self.body:
            pc = stmt.assign_pc(pc)
        return pc

    def assign_next_stmt(self, next_stmt):
        self.next_stmt = next_stmt

        block_length = len(self.body)
        for i in range(block_length - 1):
            stmt = self.body[i] 
            stmt.assign_next_stmt(self.body[i + 1])
        
        # not a type, next statement of a loop child is the loop guard
        self.body[block_length - 1].assign_next_stmt(self)

    def __str__(self):
        def branch_to_str(branch):
            return indent_string("\n".join([str(b) for b in branch]), 4)

        string = f"{self.pc}: while {self.condition}:\n{branch_to_str(self.body)}"
        return string

