from typing import Tuple, Dict
from symengine.lib.symengine_wrapper import Expr, Symbol

class MarkovState:
    state: Tuple[Tuple[Symbol, int]]
    pc: int

    def __init__(self, state: Dict[Symbol, int], pc: int):
        self.state = tuple(state.items())
        self.pc = pc

    def get_prism_encoding(self, primed: bool = False):
        prime = ""
        if primed:
            prime = "'"
        state = f"(pc{prime}={self.pc})"
        for (v, val) in self.state:
            state += f"&({v}{prime}={val})"
        return state

    def __str__(self):
        txt = "("
        for key, value in self.state:
            txt += f"{key}: {value}, "
        return txt + f"{self.pc} )"

    def __eq__(self, other):
        if self.pc != other.pc:
            return False
        
        return self.state == other.state

    def __hash__(self):
        return hash((self.pc, self.state))