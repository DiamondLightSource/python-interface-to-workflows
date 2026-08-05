"""Interface for ``python -m python_interface_to_workflows``."""

from argparse import ArgumentParser
from collections.abc import Sequence

from . import __version__

__all__ = ["main"]


def main(args: Sequence[str] | None = None) -> None:
    """Argument parser for the CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-sleep",
    )
    parser.parse_args(args)
    if "-sleep" in vars(parser.parse_args(args)):
        while True:
            import time

            time.sleep(200)


if __name__ == "__main__":
    main()
    while True:
        import time

        time.sleep(200)
