"""Refuse every HyperFrames invocation that is not a local check, render, or doctor."""

from __future__ import annotations

from hf import PIN

# The only HyperFrames subcommands this process will spawn.
HYPERFRAMES_COMMANDS = frozenset({"doctor", "check", "render"})

# Wrapper commands. poster is a local ffmpeg frame grab, not a HyperFrames call.
LOCAL_COMMANDS = HYPERFRAMES_COMMANDS | {"poster"}

# Exact argument tokens that mean a hosted, cloud, or credit path.
BANNED_TOKENS = frozenset(
    {
        "cloud",
        "publish",
        "lambda",
        "cloudrun",
        "cloud-run",
        "credits",
        "credit",
        "billing",
        "deploy",
        "login",
        "logout",
        "heygen",
    }
)


class GuardError(RuntimeError):
    pass


def _banned(token: str) -> bool:
    low = token.strip().lower()
    if low in BANNED_TOKENS:
        return True
    if low.startswith("--"):
        name = low[2:].split("=", 1)[0]
        if name in BANNED_TOKENS:
            return True
    return False


def assert_local(argv: list[str]) -> str:
    """Return the local subcommand, or raise before any process is started."""
    if not argv or not argv[0].strip():
        raise GuardError("refusing empty command; local doctor, check, render, and poster only")
    command = argv[0].strip().lower()
    if command not in LOCAL_COMMANDS:
        raise GuardError(
            f"refusing {argv[0]!r}: local doctor, check, render, and poster only"
        )
    for token in argv[1:]:
        if _banned(token):
            raise GuardError(f"refusing non-local argument {token!r}")
    return command


def assert_hyperframes(cmd: list[str]) -> None:
    """The spawned CLI must be the pinned local package and a local subcommand."""
    if len(cmd) < 4 or cmd[:3] != ["npx", "--yes", PIN]:
        raise GuardError("refusing to spawn a command that is not the pinned local HyperFrames CLI")
    if cmd[3] not in HYPERFRAMES_COMMANDS:
        raise GuardError(f"refusing HyperFrames subcommand {cmd[3]!r}")
    for token in cmd:
        if _banned(token):
            raise GuardError(f"refusing non-local argument {token!r}")
