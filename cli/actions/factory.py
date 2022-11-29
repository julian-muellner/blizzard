from argparse import Namespace

from .convert_action import Action, ConvertAction
from .print_benchmark_action import PrintBenchmarkAction


class ActionFactory:

    @classmethod
    def create_action(cls, cli_args: Namespace) -> Action:
        if cli_args.convert is not None:
            return ConvertAction(cli_args)

        return PrintBenchmarkAction(cli_args)
