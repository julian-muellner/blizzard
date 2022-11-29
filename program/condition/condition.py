from abc import ABC, abstractmethod
from typing import List, Tuple, Dict
from symengine.lib.symengine_wrapper import Expr, Symbol


class Condition(ABC):

    @abstractmethod
    def simplify(self) -> "Condition":
        pass

    @abstractmethod
    def reduce(self, store) -> List[Tuple[Symbol, Expr]]:
        pass

    @abstractmethod
    def get_free_symbols(self):
        pass

    @abstractmethod
    def get_conjuncts(self) -> List["Condition"]:
        pass

    @abstractmethod
    def subs(self, substitutions):
        pass

    @abstractmethod
    def evaluate(self, state: Dict[Symbol, float]):
        pass
