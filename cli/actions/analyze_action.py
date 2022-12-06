from argparse import Namespace
import os
import re
import time
from typing import Set
from executors import TranslationExecutor, MarkovState
from modelcheckers import ModelChecker, PrismModelChecker, StormModelChecker
from modelcheckers.modelchecker import ModelCheckingStateResult
from .action import Action
from program import Program
from cli.common import parse_program
from symengine.lib.symengine_wrapper import sympify, Symbol


class AnalyzeAction(Action):
    cli_args: Namespace
    program: Program

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        self.program = parse_program(benchmark)

        # make sure all target variables are program variables
        if len(self.cli_args.analyze) == 0:
            target_variables = self.program.variables
        else:
            target_variables = {sympify(v) for v in self.cli_args.analyze}
            if not self.program.variables.issuperset(target_variables):
                raise Exception(f"Analyze variables are not proper program variables.")

        conversion = TranslationExecutor(self.program, enable_sink=False, analyze_vars=target_variables)
        prism = conversion.convertProgram()

        print(f"Resulting program has {conversion.get_num_states()} states")

        tmp_folder = "./run_" + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        os.mkdir(tmp_folder)
        tmp_prism = tmp_folder + "/model.prism"
        with open(tmp_prism, "w") as f:
            f.write(prism)

        is_valid = lambda var, val: (val >= self.program.get_type(var).lower) and (val <= self.program.get_type(var).upper)
        if self.cli_args.checker == "prism":
            mc = PrismModelChecker(is_valid)
        elif self.cli_args.checker == "storm":
            mc = StormModelChecker(is_valid)
        else:
            raise Exception("Unsupported Model Checker specified!")

        results = None
        if self.cli_args.style == "steadystate":
            results = self.__analyze_steadystate__(mc, tmp_prism, self.program.symbols, tmp_folder, self.program.max_pc, conversion.violation_state.pc)
        elif self.cli_args.style == "property":
            results = self.__analyze_property__(mc, tmp_prism, self.program.symbols, conversion.terminal_states, conversion.violation_state.pc)
        else:
            raise Exception("Unsupported Query style specified!")


        if results is not None:
            for result in results:
                print(str(result))
                
            if self.cli_args.out is not None:
                with open(self.cli_args.out, "w") as f:
                    for result in results:
                        f.write(str(result) + "\n")

        os.remove(tmp_prism)
        os.rmdir(tmp_folder)

    def __analyze_steadystate__(self, mc: ModelChecker, prismfile: str, symbols: Set[Symbol], folder: str, target_pc: int, violation_pc: int):
        return mc.analyzeSteadyState(prismfile, symbols, folder, target_pc, violation_pc)

    def __analyze_property__(self, mc: ModelChecker, prismfile: str, symbols: Set[Symbol], terminal_states: Set[MarkovState], violation_pc: int):

        # compute query for each terminal state, map back to original state
        mapping = dict((f"P=? [ F {s.get_prism_encoding()} ]", s) for s in terminal_states)
        mc_results = mc.analyzeProperties(prismfile, symbols, mapping.keys())

        if mc_results is None:
            return None

        results = []
        for (prop, probability) in mc_results:
            mc_state = mapping[prop]
            if mc_state.pc == violation_pc:
                if re.fullmatch(r"0+(\.0*)?", probability) is None: # check if 0.0 or 0
                    results.append(ModelCheckingStateResult({}, probability, is_violation=True))
            else:
                result = dict((var, value) for var, value in mc_state.state if mc.is_valid(var, value)) # remove uninit vars
                results.append(ModelCheckingStateResult(result, probability))
        return results
