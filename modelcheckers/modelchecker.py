from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

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
            for key, value in self.state:
                txt += f"{key}: {value}, "
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
    @abstractmethod
    def analyzeSteadyState(self, inputfile: str, tmp_folder: str, target_pc: int, violation_pc: int) -> List[ModelCheckingStateResult]:
        pass

    @abstractmethod
    def analyzeProperties(self, properties: List[str]) -> List[Tuple[str, float]]:
        pass
