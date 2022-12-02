from typing import Set
from symengine.lib.symengine_wrapper import Symbol

from .executor import Executor
from .markovchain import MarkovChain, MarkovState

from program.ifstatem import IfStatem
from program.observestatem.observestatem import ObserveStatem
from program.program import Program
from program.type.finite_range import FiniteRange
from program.whilestatem import WhileStatem
from program.assignment.dist_assignment import DistAssignment
from program.assignment.poly_assignment import PolyAssignment
from program.endstatem.endstatem import EndStatem

######################################
# Notes regarding the encoding:      #
######################################
# The state encoding is quite obvious, but the pc always talks about the line AFTER execution

# Initial state: every program variable is set to lower_bound - 1, pc is set to 0
#   (So that we can detect if a variable might be uninitialized at the end)

# Terminal states: PC = program.max_pc
# Violation state: PC = -1; all variables = lower bound - 1
# Sink state: PC = program.max_pc + 1; all variables = lower bound - 1

###############################################
# Notes regarding the state memoization:      #
###############################################
# To avoid endless looping, we check if we have seen a state before.
# We do so at while loops and distribution assignments 
# There may be room for improvement by dropping variables that
#   1. go out of scope
#   2. are overwritten in the next loop iteration

class TranslationExecutor(Executor):
    """Class to translate a program into either an absorbing or a sinking Markov chain"""
    terminal_states: Set[MarkovState]
    mc: MarkovChain
    program: Program
    violation_state: MarkovState # state where violated assertions go
    enable_sink: bool
    sink_state: MarkovState # state where everything is going in the end if enable_sink is defined

    def __init__(self, program: Program, enable_sink=False):
        self.mc = MarkovChain()
        self.terminal_states = set()
        self.program = program
        self.enable_sink = enable_sink

    def convertProgram(self):
        # empty state
        empty_state =  {}
        for v in self.program.variables:
            assert(isinstance(self.program.get_type(v), FiniteRange))
            empty_state[v] = self.program.get_type(v).lower - 1

        # sink state
        lower_pc = -1
        upper_pc = self.program.max_pc
        if self.enable_sink:
            self.sink_state = MarkovState(empty_state, self.program.max_pc + 1)
            self.mc.add_state(self.sink_state)
            self.mc.add_transition(self.sink_state, self.sink_state, 1)
            upper_pc = self.program.max_pc + 1

        # construct violation state
        self.violation_state = MarkovState(empty_state, -1)
        self.mc.add_state(self.violation_state)
        self.terminal_states.add(self.violation_state)
        if self.enable_sink:
            self.mc.add_transition(self.violation_state, self.sink_state, 1)
        else:
            self.mc.add_transition(self.violation_state, self.violation_state, 1)
        
        # kick off execution
        stmt = self.program.statements[0]
        initial = MarkovState(empty_state, stmt.pc - 1)
        self.mc.add_state(initial)
        self.execute(stmt, (empty_state, initial))

        # extract prism model
        return self.mc.convert_to_prism(self.program, lower_pc, upper_pc)

    def executeIf(self, stmt: IfStatem, ctx):
        state, _ = ctx
        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.if_branch[0], ctx)]
        elif stmt.else_branch:
            return [(stmt.else_branch[0], ctx)]
        else:
            return [(stmt.next_stmt, ctx)]

    def executeWhile(self, stmt: WhileStatem, ctx):
        state, pred = ctx

        # loops need to check state in case state is not modified in body
        mc_state = MarkovState(state, stmt.pc)
        self.mc.add_transition(pred, mc_state, 1)
        if self.mc.has_state(mc_state):
            return []
        self.mc.add_state(mc_state)

        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.body[0], (state, mc_state))]
        else:
            return [(stmt.next_stmt, (state, mc_state))]

    def executeDistAssign(self, stmt: DistAssignment, ctx):
        state, pred = ctx
        possible_values = stmt.distribution.get_support_with_probability()
        continuations = []
        
        for (val, prob) in possible_values:
            state_copy = state.copy()
            self.__assert_variable_constraints__(stmt.variable, val)
            state_copy[stmt.variable] = val
            mc_state = MarkovState(state_copy, stmt.pc)

            self.mc.add_transition(pred, mc_state, prob)
            if self.mc.has_state(mc_state):
                continue

            self.mc.add_state(mc_state)
            continuations.append((stmt.next_stmt, (state_copy, mc_state)))
        return continuations

    def executePolyAssign(self, stmt: PolyAssignment, ctx):
        state, pred = ctx

        e = stmt.evaluate_right_side(state)
        self.__assert_variable_constraints__(stmt.variable, e)
        state[stmt.variable] = int(e)
        return [(stmt.next_stmt, (state, pred))]

    def executeObserve(self, stmt: ObserveStatem, ctx):
        state, pred = ctx
        cond = stmt.condition.evaluate(state)
        if cond:
            return [(stmt.next_stmt, ctx)]
        else:
            self.mc.add_transition(pred, self.violation_state, 1)
            return []

    def executeEnd(self, stmt: EndStatem, ctx):
        # add tranistion into end state, only change PC
        state, pred = ctx
        mc_state = MarkovState(state, stmt.pc)
        self.mc.add_transition(pred, mc_state, 1)
        self.mc.add_state(mc_state)
        self.terminal_states.add(mc_state)

        # specialization decides what to do with terminal states
        if self.enable_sink:
            self.mc.add_transition(mc_state, self.sink_state, 1)
        else:
            self.mc.add_transition(mc_state, mc_state, 1)
        return []

    def get_num_states(self):
        return self.mc.get_num_states()

    def __str__(self):
        return str(self.mc)

    def __assert_variable_constraints__(self, variable: Symbol, value: int):
        if not value.is_integer:
            raise Exception(f"Variable {variable} is assigned non-integer value {value}")
        t = self.program.get_type(variable)
        if not (value >= t.lower and value <= t.upper):
            raise Exception(f"Variable {variable} is assigned value {value} out of its declared range!")
