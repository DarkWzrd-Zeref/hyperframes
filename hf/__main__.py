"""CLI for the local render wrapper. Entry point: ./render.sh"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from hf.guard import GuardError, assert_local
from hf.local import check_cmd, doctor_cmd, poster_cmd, render_cmd


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="render.sh",
        description="Local HyperFrames check and render. Cloud and credit paths are refused.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor", help="check the local Node, Chrome, and FFmpeg toolchain")

    check = sub.add_parser("check", help="hyperframes check on a composition directory")
    check.add_argument("composition", type=Path)

    render = sub.add_parser("render", help="local hyperframes render to an MP4")
    render.add_argument("composition", type=Path)
    render.add_argument("--output", required=True, type=Path)
    render.add_argument("--fps", type=int, default=30)

    poster = sub.add_parser("poster", help="grab one JPG frame with local ffmpeg")
    poster.add_argument("mp4", type=Path)
    poster.add_argument("--output", required=True, type=Path)
    poster.add_argument("--at", type=float, default=2.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    raw = list(sys.argv[1:] if argv is None else argv)
    if any(token in {"-h", "--help"} for token in raw):
        _parser().parse_args(raw)
        return 0
    try:
        assert_local(raw)
        args = _parser().parse_args(raw)
        if args.command == "doctor":
            _run(doctor_cmd())
        elif args.command == "check":
            if not args.composition.is_dir():
                print(f"composition directory not found: {args.composition}", file=sys.stderr)
                return 2
            _run(check_cmd(args.composition))
        elif args.command == "render":
            if not args.composition.is_dir():
                print(f"composition directory not found: {args.composition}", file=sys.stderr)
                return 2
            args.output.parent.mkdir(parents=True, exist_ok=True)
            _run(render_cmd(args.composition, args.output, args.fps))
        elif args.command == "poster":
            if not args.mp4.is_file():
                print(f"mp4 not found: {args.mp4}", file=sys.stderr)
                return 2
            args.output.parent.mkdir(parents=True, exist_ok=True)
            cmd = poster_cmd(args.mp4, args.output, args.at)
            if cmd[0] != "ffmpeg":
                print("refusing poster command that is not ffmpeg", file=sys.stderr)
                return 2
            _run(cmd)
        else:
            print(f"refusing {args.command!r}", file=sys.stderr)
            return 2
    except GuardError as err:
        print(str(err), file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as err:
        return err.returncode or 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
