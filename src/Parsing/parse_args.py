"""Parse the command-line arguments used to locate the game configuration."""

from argparse import ArgumentParser, ArgumentError
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Args:
    """Read and validate the command-line configuration-file argument."""

    @property
    def get_args(self) -> str:
        """Return the contents of the expected configuration file."""
        parser = ArgumentParser()
        path_file = Path.cwd() / "config.json"
        if not path_file.exists():
            raise FileNotFoundError("Error: config.json is missing")
        parser.add_argument("config_json", help=str(path_file))
        args = parser.parse_args()
        if args.config_json != "config.json":
            raise ArgumentError(
                None, 'Error: wrong file name (should be "config.json")'
            )
        return path_file.read_text(encoding="utf-8")
