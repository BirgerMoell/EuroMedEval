"""Command-line interface for EuroMedEval."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .builders import build_all, build_dataset
from .registry import get_dataset_config, list_dataset_configs


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(prog="euromedeval")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-datasets", help="List dataset configs.")
    list_parser.add_argument("--language", help="Filter by language code, e.g. sv.")

    show_parser = subparsers.add_parser("show-dataset", help="Show one dataset config.")
    show_parser.add_argument("name", help="Dataset config name.")

    build_parser = subparsers.add_parser("build-dataset", help="Run the creation script for one dataset.")
    build_parser.add_argument("name", help="Dataset config name.")

    build_all_parser = subparsers.add_parser("build-all", help="Run the creation scripts for all datasets.")
    build_all_parser.add_argument("--language", help="Filter builds by language code, e.g. sv.")
    return parser


def main() -> None:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list-datasets":
        configs = list_dataset_configs(language=args.language)
        for config in configs:
            print(
                f"{config.name}\t{config.language}\t{config.country}\t"
                f"{config.task}\t{config.record_format}\t{config.status}\t{config.tier}"
            )
        return

    if args.command == "show-dataset":
        config = get_dataset_config(name=args.name)
        print(json.dumps(asdict(config), indent=2))
        return

    if args.command == "build-dataset":
        script_path = build_dataset(args.name)
        print(f"Built {args.name} using {script_path}")
        return

    if args.command == "build-all":
        built = build_all(language=args.language)
        for name in built:
            print(name)
        return

    raise ValueError(f"Unsupported command: {args.command}")
