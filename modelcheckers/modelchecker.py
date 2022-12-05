from abc import ABC, abstractmethod
from argparse import Namespace
from typing import Callable, Dict, List, Tuple

from symengine.lib.symengine_wrapper import Expr, Symbol

class ModelCheckingStateResult:
    state: Tuple[Tuple[str, int]]
    probability: float
    is_violation: bool

    def __init__(self, state: Dict[str, int], prob: float, is_violation: bool = False):
        self.state = tuple(state.items())
        self.probability = prob
        self.is_violation = is_violation

    def __str__(self):
        txt = "("
        if self.is_violation:
            txt += "observation-violation"
        else:
            for i, (key, value) in enumerate(self.state):
                if i == 0:
                    txt += f"{key}: {value}"
                else:
                    txt += f", {key}: {value}"
        return txt + f"): {self.probability}"

    def __eq__(self, other):
        if self.is_violation != other.is_violation:
            return False

        if self.probability != other.probability:
            return False
        
        return self.state == other.state

    def __hash__(self):
        return hash((self.probability, self.state, self.is_violation))

class ModelChecker(ABC):
    is_valid: Callable[[str, int], bool] # returns true iff the value indicates that the variable is initialized

    def __init__(self, is_valid: Callable[[str, int], bool]):
        self.is_valid = is_valid

    @abstractmethod
    def analyzeSteadyState(self, inputfile: str, tmp_folder: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        pass

    @abstractmethod
    def analyzeProperties(self, properties: List[str]) -> List[Tuple[str, float]]:
        pass

