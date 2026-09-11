from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from .register import load_register, render_markdown


def main() -> None:
    parser = argparse.ArgumentParser(description="Assess a risk acceptance register")
    parser.add_argument("input", help="Path to register JSON")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Assessment date (YYYY-MM-DD)")
    parser.add_argument("--output", help="Optional Markdown report output path")
    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of)
    records = load_register(args.input)
    report = render_markdown(records, as_of)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
