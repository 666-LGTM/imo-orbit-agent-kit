from __future__ import annotations

import argparse
from pathlib import Path

from .agents import run_workflow
from .config import load_config
from .llm import MiMoChatClient, MockMiMoClient
from .report import write_report
from .server import serve


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orbit-agent-kit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run the multi-agent workflow")
    run_parser.add_argument("--idea", required=True, help="project idea to analyze")
    run_parser.add_argument("--out", default="reports/demo", help="output directory")
    run_parser.add_argument("--live", action="store_true", help="use Xiaomi MiMo API")

    serve_parser = subparsers.add_parser("serve", help="serve a generated report")
    serve_parser.add_argument("--dir", default="reports/demo", help="report directory")
    serve_parser.add_argument("--port", type=int, default=8765, help="local port")

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)

    if args.command == "run":
        config = load_config()
        client = MiMoChatClient(config) if args.live else MockMiMoClient(config.model)
        result = run_workflow(args.idea, client)
        out_dir = Path(args.out)
        write_report(result, out_dir)
        print(f"Generated evidence pack in {out_dir}")
        print(f"Mode: {'live' if result.live else 'mock'}")
        print(f"Estimated tokens: {result.total_tokens:,}")
        return

    if args.command == "serve":
        serve(Path(args.dir), args.port)


if __name__ == "__main__":
    main()
