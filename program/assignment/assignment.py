from abc import ABC, abstractmethod
from typing import Union, Tuple, Set, Dict

from symengine.lib.symengine_wrapper import Expr, Symbol

from .exceptions import EvaluationException


class Assignment(ABC):
    variable: Symbol  # the variable to assign to
    pc: int # program counter

    def __init__(self, variable):
        self.variable = Symbol(str(variable))
        self.pc = -1
        self.next_stmt = None

    def evaluate(self, state: Dict[Symbol, float]):
        result = self.evaluate_right_side(state)
        state[self.variable] = int(result)
        return state

    def assign_pc(self, pc) -> int:
        self.pc = pc
        return pc + 1

    def assign_next_stmt(self, next_stmt):
        self.next_stmt = next_stmt

    @abstractmethod
    def subs(self, substitutions):
        pass

    @abstractmethod
    def evaluate_right_side(self, state: Dict[Symbol, float]):
        pass

    @abstractmethod
    def get_free_symbols(self) -> Set[Symbol]:
        """
        Returns the free symbols in the assignments right side.
        """
