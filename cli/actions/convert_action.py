from argparse import Namespace
from cli.argument_parser import ArgumentParser
from executors.sink_translation import SinkTranslation
from executors.absorbing_translation import AbsorbingTranslation
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
        conversion = AbsorbingTranslation(program)
        prism = conversion.convertProgram()
        print(program)
        print("\n" * 1 + "#" * 80 + "\n" * 1)
        print(prism)
        print("\n" + "#" * 80 + "\n")
        print(f"Resulting program has {len(conversion.states)} states")
        with open(result_filename, "w") as f:
            f.write(prism)
