from argparse import Namespace

from .analyze_action import AnalyzeAction
from .convert_action import Action, ConvertAction
from .print_benchmark_action import PrintBenchmarkAction


class ActionFactory:

    @classmethod
    def create_action(cls, cli_args: Namespace) -> Action:
        if cli_args.convert is not None:
            return ConvertAction(cli_args)
        if cli_args.analyze is not None:
            return AnalyzeAction(cli_args)

        return PrintBenchmarkAction(cli_args)
