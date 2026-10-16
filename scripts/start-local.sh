#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_VENV_UVICORN="$ROOT_DIR/backend/venv/bin/uvicorn"

if [[ -x "$BACKEND_VENV_UVICORN" ]]; then
  BACKEND_RUNNER="$BACKEND_VENV_UVICORN"
elif command -v uvicorn >/dev/null 2>&1; then
  BACKEND_RUNNER="$(command -v uvicorn)"
else
  echo "uvicorn is missing. Install backend/requirements.txt first." >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is missing. Install Node.js and npm first." >&2
  exit 1
fi

BACKEND_PID=""
WEB_PID=""
cleanup() {
  [[ -z "$BACKEND_PID" ]] || kill "$BACKEND_PID" 2>/dev/null || true
  [[ -z "$WEB_PID" ]] || kill "$WEB_PID" 2>/dev/null || true
  [[ -z "$BACKEND_PID" ]] || wait "$BACKEND_PID" 2>/dev/null || true
  [[ -z "$WEB_PID" ]] || wait "$WEB_PID" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

(cd "$ROOT_DIR/backend" && "$BACKEND_RUNNER" app.main:app --reload --port 8000) &
BACKEND_PID=$!
(cd "$ROOT_DIR/web" && npm run dev) &
WEB_PID=$!

echo "IRL LootDrop running: frontend http://localhost:3000 | backend http://localhost:8000"
wait "$BACKEND_PID" "$WEB_PID"
