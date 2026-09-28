#!/usr/bin/env bash
# Local HyperFrames render wrapper. Refuses cloud, HeyGen hosted, and credit paths.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${ROOT}${PYTHONPATH:+:${PYTHONPATH}}"
exec python3 -m hf "$@"
