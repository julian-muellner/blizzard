from program.condition import Condition
from utils import indent_string


class ObserveStatem:
    condition: Condition
    if_branch = None
    else_branch = None
    pc: int

    def __init__(self, condition):
        self.condition = condition
        self.pc = -1
        self.next_stmt = None

    def assign_pc(self, pc) -> int:
        self.pc = pc
        return pc + 1

    def assign_next_stmt(self, next_stmt):
        self.next_stmt = next_stmt

    def __str__(self):
        string = f"{self.pc}: observe {self.condition}"
        return string
