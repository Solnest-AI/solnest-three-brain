#!/usr/bin/env bash
# grok-consult.sh: ask Grok Build (the logged-in `grok` CLI) for a second opinion, safely.
#
# Why this exists: Grok's built-in `read-only` and `strict` sandbox profiles can refuse to
# start on macOS when /var/run/docker.sock is a symlink (Docker Desktop does this). The
# official Claude Code plugin (grok-build@xai-grok-build) hardcodes `--sandbox read-only` and
# auto-approves every tool call, so its review/critique commands fail on those machines.
# The `workspace` sandbox works: Grok can read anywhere but only write inside its working
# directory. We point that working directory at a THROWAWAY COPY of the files, so the worst
# a consult can do is edit the copy, and the copy is deleted when the run ends.
#
# Usage:
#   grok-consult.sh <source_dir> "<prompt>" [output_file]
# Env:
#   GROK_CONSULT_MODEL   optional model override (default: grok's own default model)
set -euo pipefail

src="${1:?usage: grok-consult.sh <source_dir> <prompt> [output_file]}"
prompt="${2:?missing prompt}"
out="${3:-}"
[[ -d "$src" ]] || { echo "not a directory: $src" >&2; exit 2; }
command -v grok >/dev/null || { echo "grok CLI not on PATH. Install: curl -fsSL https://x.ai/cli/install.sh | bash" >&2; exit 3; }
command -v rsync >/dev/null || { echo "rsync is required" >&2; exit 3; }

# Capture first: piping `grok models` into `grep -q` under pipefail SIGPIPEs grok and reads
# as "not logged in". The status line prints to stderr, so merge it in.
# The probe can transiently say "not authenticated" while grok refreshes a near-expiry token,
# so give it three tries before giving up.
auth_status=""
for _attempt in 1 2 3; do
  auth_status="$(grok models 2>&1 || true)"
  [[ "$auth_status" == *"logged in with"* ]] && break
  sleep 2
done
[[ "$auth_status" == *"logged in with"* ]] || { echo "grok is not logged in: run 'grok login --oauth'" >&2; exit 4; }

work="$(mktemp -d "${TMPDIR:-/tmp}/grok-consult.XXXXXX")"
trap 'rm -rf "$work"' EXIT

# Copy the material, skipping heavy or irrelevant folders. Never copy .env files.
rsync -a --exclude '.git' --exclude 'node_modules' --exclude '.venv' --exclude '__pycache__' \
  --exclude '.env' --exclude '.env.*' "$src"/ "$work"/

model_args=()
[[ -n "${GROK_CONSULT_MODEL:-}" ]] && model_args=(-m "$GROK_CONSULT_MODEL")

full_prompt="You are consulting as a second-opinion reviewer. The files are a COPY of the real project; do not try to edit them, answer only. ${prompt}"
# ${model_args[@]+"${model_args[@]}"} keeps `set -u` happy on the bash 3.2 that ships with macOS.
if [[ -n "$out" ]]; then
  (cd "$work" && grok -p "$full_prompt" --sandbox workspace --always-approve --output-format plain ${model_args[@]+"${model_args[@]}"}) > "$out"
  echo "grok answer written to $out ($(wc -w < "$out" | tr -d ' ') words)"
else
  (cd "$work" && grok -p "$full_prompt" --sandbox workspace --always-approve --output-format plain ${model_args[@]+"${model_args[@]}"})
fi
