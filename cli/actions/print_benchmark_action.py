from argparse import Namespace
from termcolor import colored

from inputparser import Parser
from .action import Action
from cli.common import parse_program


class PrintBenchmarkAction(Action):
    cli_args: Namespace

    def __init__(self, cli_args: Namespace):
        self.cli_args = cli_args

    def __call__(self, *args, **kwargs):
        benchmark: str = args[0]
        program = parse_program(benchmark)

        print(colored("------------------", "magenta"))
        print(colored("- Parsed program -", "magenta"))
        print(colored("------------------", "magenta"))
        print(program)
        print()
