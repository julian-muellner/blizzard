from abc import ABC, abstractmethod

from program.ifstatem import IfStatem
from program.endstatem.endstatem import EndStatem
from program.observestatem.observestatem import ObserveStatem
from program.whilestatem import WhileStatem
from program.assignment.dist_assignment import DistAssignment
from program.assignment.poly_assignment import PolyAssignment


class Executor(ABC):
    @abstractmethod
    def executeIf(self, stmt: IfStatem, ctx):
        pass

    @abstractmethod
    def executeWhile(self, stmt: WhileStatem, ctx):
        pass

    @abstractmethod
    def executeDistAssign(self, stmt: DistAssignment, ctx):
        pass

    @abstractmethod
    def executePolyAssign(self, stmt: PolyAssignment, ctx):
        pass

    @abstractmethod
    def executeObserve(self, stmt: ObserveStatem, ctx):
        pass

    @abstractmethod
    def executeEnd(self, stmt: EndStatem, ctx):
        pass

    def execute(self, stmt, ctx):
        if isinstance(stmt, PolyAssignment):
            self.executePolyAssign(stmt, ctx)
        elif isinstance(stmt, DistAssignment):
            self.executeDistAssign(stmt, ctx)
        elif isinstance(stmt, IfStatem):
            self.executeIf(stmt, ctx)
        elif isinstance(stmt, WhileStatem):
            self.executeWhile(stmt, ctx)
        elif isinstance(stmt, ObserveStatem):
            self.executeObserve(stmt, ctx)
        elif isinstance(stmt, EndStatem):
            self.executeEnd(stmt, ctx)
        else:
            raise Exception("Visiting unknown Statement")
