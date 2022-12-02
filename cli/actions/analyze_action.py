from argparse import Namespace
import os
import time
from cli.argument_parser import ArgumentParser
from executors import TranslationExecutor
from inputparser.parser import Parser
from modelcheckers import StormModelChecker
from modelcheckers import PrismModelChecker
from .action import Action
from program import Program
from cli.common import parse_program


class AnalyzeAction(Action):
    cli_args: Namespace
    program: Program

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]

        tmp_folder = "./run_" + time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        os.mkdir(tmp_folder)

        tmp_prism = tmp_folder + "/model.prism"

        result_filename = self.cli_args.convert
        program = parse_program(benchmark)
        conversion = TranslationExecutor(program, enable_sink=False)
        prism = conversion.convertProgram()

        print(f"Resulting program has {conversion.get_num_states()} states")

        with open(tmp_prism, "w") as f:
            f.write(prism)

        # TODO: let user select PMC
        # TODO: let use pass properties
        mc = StormModelChecker()
        # results = mc.analyzeSteadyState(tmp_prism, tmp_folder, program.max_pc, conversion.violation_state.pc)
        # if results is not None:
        #     with open(self.cli_args.analyze, "w") as f:
        #         for result in results:
        #             f.write(str(result) + "\n")

        properties = [
            "P=? [ F (pc=8)&(x=5)]",
            "P=? [ F (pc=8)&(x=6)]",
            "P=? [ F (pc=8)&(x=7)]",
            "P=? [ F (pc=8)&(x=0)]",
            "P=? [ F (pc=8)&(x=-1)]",
        ]
        results = mc.analyzeProperties(tmp_prism, properties)

        if results is not None:
            with open(self.cli_args.analyze, "w") as f:
                for (prop, result) in results:
                    f.write(f"{prop} -> {result}\n")

        os.remove(tmp_prism)
        os.rmdir(tmp_folder)
