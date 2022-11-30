from abc import ABC, abstractmethod
from collections import deque
from typing import Any, List, Tuple

from program.ifstatem import IfStatem
from program.endstatem.endstatem import EndStatem
from program.observestatem.observestatem import ObserveStatem
from program.whilestatem import WhileStatem
from program.assignment.dist_assignment import DistAssignment
from program.assignment.poly_assignment import PolyAssignment

# execute methods shall return a tuple (next_stmt, ctx)
# where next_stmt is the next statement to be executed and ctx the corresponding context.
# they may also return a list of such tuples

continuation = Tuple[Any, Any]

class Executor(ABC):
    @abstractmethod
    def executeIf(self, stmt: IfStatem, ctx) -> List[continuation]:
        pass

    @abstractmethod
    def executeWhile(self, stmt: WhileStatem, ctx) -> List[continuation]:
        pass

    @abstractmethod
    def executeDistAssign(self, stmt: DistAssignment, ctx) -> List[continuation]:
        pass

    @abstractmethod
    def executePolyAssign(self, stmt: PolyAssignment, ctx) -> List[continuation]:
        pass

    @abstractmethod
    def executeObserve(self, stmt: ObserveStatem, ctx) -> List[continuation]:
        pass

    @abstractmethod
    def executeEnd(self, stmt: EndStatem, ctx) -> List[continuation]:
        pass

    def execute(self, start, ctx):
        stack = deque([(start, ctx)])
        while stack:
            (stmt, ctx) = stack.pop()
            results = self.executeStep(stmt, ctx)
            stack.extend(results)

    # execute all the statements
    def executeStep(self, stmt, ctx) -> List[continuation]:
        if isinstance(stmt, PolyAssignment):
            return self.executePolyAssign(stmt, ctx)
        elif isinstance(stmt, DistAssignment):
            return self.executeDistAssign(stmt, ctx)
        elif isinstance(stmt, IfStatem):
            return self.executeIf(stmt, ctx)
        elif isinstance(stmt, WhileStatem):
            return self.executeWhile(stmt, ctx)
        elif isinstance(stmt, ObserveStatem):
            return self.executeObserve(stmt, ctx)
        elif isinstance(stmt, EndStatem):
            return self.executeEnd(stmt, ctx)
        else:
            raise Exception("Visiting unknown Statement")
