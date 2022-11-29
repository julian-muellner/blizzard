
from typing import Any

class EndStatem:
    pc: int

    def __init__(self):
        self.pc = -1

    def assign_pc(self, pc) -> int:
        self.pc = pc
        return pc + 1

    def __str__(self):
        string = f"{self.pc}: "
        return string

