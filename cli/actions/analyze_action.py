from argparse import Namespace
import os
import time
from executors import TranslationExecutor
from modelcheckers import ModelChecker, PrismModelChecker, StormModelChecker
from .action import Action
from program import Program
from cli.common import parse_program
from symengine.lib.symengine_wrapper import sympify


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
                raise Exception(f"Conversion variables are not proper program variables.")

        conversion = TranslationExecutor(self.program, enable_sink=False, analyze_vars=target_variables)
        prism = conversion.convertProgram()

        print(f"Resulting program has {conversion.get_num_states()} states")

        tmp_folder = "./run_" + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        os.mkdir(tmp_folder)
        tmp_prism = tmp_folder + "/model.prism"
        with open(tmp_prism, "w") as f:
            f.write(prism)

        if self.cli_args.checker == "prism":
            mc = PrismModelChecker()
        elif self.cli_args.checker == "storm":
            mc = StormModelChecker()
        else:
            raise Exception("Unsupported Model Checker specified!")

        if self.cli_args.style == "steadystate":
            self.__analyze_steadystate__(mc, tmp_prism, tmp_folder, self.program.max_pc, conversion.violation_state.pc)
        elif self.cli_args.style == "property":
            self.__analyze_property__(mc, tmp_prism)
        else:
            raise Exception("Unsupported Query style specified!")

        os.remove(tmp_prism)
        os.rmdir(tmp_folder)

    def __analyze_steadystate__(self, mc: ModelChecker, prismfile: str, folder: str, target_pc: int, violation_pc: int):
        results = mc.analyzeSteadyState(prismfile, folder, target_pc, violation_pc)
        if results is not None:
            for result in results:
                print(str(result))
                
            if self.cli_args.out is not None:
                with open(self.cli_args.out, "w") as f:
                    for result in results:
                        f.write(str(result) + "\n")

    def __analyze_property__(self, mc: ModelChecker, prismfile: str):
        properties = [
            "P=? [ F (pc=8)&(x=5)]",
            "P=? [ F (pc=8)&(x=6)]",
            "P=? [ F (pc=8)&(x=7)]",
            "P=? [ F (pc=8)&(x=0)]",
            "P=? [ F (pc=8)&(x=-1)]",
        ]
        results = mc.analyzeProperties(prismfile, properties)

        if results is not None:
            for (prop, result) in results:
                    print(f"{prop} -> {result}")
                
            if self.cli_args.out is not None:
                with open(self.cli_args.out, "w") as f:
                    for (prop, result) in results:
                        f.write(f"{prop} -> {result}\n")
