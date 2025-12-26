"""CLI entrypoint.

Pure interface layer - no business logic here.
Delegates all work to application use cases.
"""
import argparse
import sys
from pathlib import Path

from mangatrans.application.usecases import translate_page
from mangatrans.infrastructure.exporters import export_to_json


def main() -> int:
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        prog="mangatrans",
        description="Manga/Manhwa translator - V1 (stub implementation)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # translate subcommand
    translate_parser = subparsers.add_parser(
        "translate", help="Translate a manga/manhwa page"
    )
    translate_parser.add_argument("image", type=Path, help="Input image path")
    translate_parser.add_argument(
        "-o", "--output", type=Path, required=True, help="Output JSON path"
    )
    translate_parser.add_argument(
        "--src", default="ja", help="Source language (default: ja)"
    )
    translate_parser.add_argument(
        "--tgt", default="en", help="Target language (default: en)"
    )

    args = parser.parse_args()

    if args.command != "translate":
        parser.print_help()
        return 1

    # Validate input
    if not args.image.exists():
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        return 1

    # Delegate to use case (no business logic here)
    result = translate_page(
        image_path=args.image,
        source_lang=args.src,
        target_lang=args.tgt,
    )

    # Export result
    export_to_json(result, args.output)

    print(f"✓ Translation result exported to: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())