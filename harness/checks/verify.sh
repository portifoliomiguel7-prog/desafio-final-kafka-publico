#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
exec "${PYTHON:-python}" "$ROOT/harness/checks/public-candidate-check.py" "$@"
