import argparse
import sys
from pathlib import Path

from .registry import NoAutobotAvailable, OptimusPrime

BANNER = "Transformers-v1 -- Autobots, transform!"

DEFAULT_SUFFIX = {
    "json": ".json",
    "yaml": ".yaml",
    "csv": ".csv",
    "markdown": ".md",
    "html": ".html",
    "python": ".py",
    "python-min": ".min.py",
    "python-pretty": ".pretty.py",
}


def _cmd_list_bots(prime: OptimusPrime) -> int:
    print("Autobots ready to roll out:")
    for bot in prime.bots:
        conversions = ", ".join(f"{f} -> {t}" for f, t in sorted(bot.conversions))
        print(f"  {bot.name:<10} {conversions}")
    return 0


def _cmd_transform(prime: OptimusPrime, args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    from_format = args.from_format or prime.detect_format(str(input_path))
    to_format = args.to

    try:
        bot = prime.find_bot(from_format, to_format)
    except NoAutobotAvailable as exc:
        print(f"No Autobot available: {exc}")
        return 1

    print(f"Optimus Prime scanning {input_path.name}... detected: {from_format}")
    print(f"Rolling out {bot.name} ({from_format} -> {to_format})...")

    content = input_path.read_text()
    result = bot.transform(content, from_format, to_format)

    if args.output:
        output_path = Path(args.output)
    else:
        suffix = DEFAULT_SUFFIX.get(to_format, f".{to_format}")
        output_path = input_path.with_name(input_path.stem + suffix)
    output_path.write_text(result)
    print(f"Wrote {output_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="transformers-v1", description=BANNER)
    subparsers = parser.add_subparsers(dest="command", required=True)

    transform_parser = subparsers.add_parser(
        "transform", help="Transform a file from one format to another"
    )
    transform_parser.add_argument("input", help="Path to the input file")
    transform_parser.add_argument(
        "--to",
        required=True,
        help="Target format (e.g. json, yaml, csv, markdown, html, python-min, python-pretty)",
    )
    transform_parser.add_argument(
        "--from",
        dest="from_format",
        default=None,
        help="Source format (auto-detected from the file extension if omitted)",
    )
    transform_parser.add_argument(
        "-o", "--output", default=None, help="Output file path (defaults next to the input file)"
    )

    subparsers.add_parser("list-bots", help="List every Autobot and the conversions it supports")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    prime = OptimusPrime()

    if args.command == "list-bots":
        return _cmd_list_bots(prime)
    if args.command == "transform":
        return _cmd_transform(prime, args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
