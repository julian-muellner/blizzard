from argparse import Namespace
from cli.argument_parser import ArgumentParser
from executors import TranslationExecutor
from inputparser.parser import Parser
from .action import Action
from program import Program
from cli.common import parse_program


class ConvertAction(Action):
    cli_args: Namespace
    program: Program

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark = args[0]
        result_filename = self.cli_args.convert
        program = parse_program(benchmark)
        conversion = TranslationExecutor(program, enable_sink=False)
        prism = conversion.convertProgram()
        print(program)
        print("\n" * 1 + "#" * 80 + "\n" * 1)
        print(prism)
        print("\n" + "#" * 80 + "\n")
        print(f"Resulting program has {conversion.get_num_states()} states")
        with open(result_filename, "w") as f:
            f.write(prism)
