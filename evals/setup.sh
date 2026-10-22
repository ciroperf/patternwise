#!/usr/bin/env bash
# Copy the test cases into a sandbox, each one its own git repo, so you can run the skill,
# inspect the diff, and reset. Usage: bash evals/setup.sh [SANDBOX_DIR]
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
sandbox="${1:-$here/../../patternwise-sandbox}"

mkdir -p "$sandbox"
for case_dir in "$here"/cases/*/; do
  name="$(basename "$case_dir")"
  target="$sandbox/$name"
  rm -rf "$target"
  cp -r "$case_dir" "$target"
  git -C "$target" init -q
  git -C "$target" -c core.autocrlf=false add -A
  git -C "$target" -c user.name=patternwise -c user.email=patternwise@example.invalid \
    commit -q -m "baseline"
  echo "ready: $target"
done
echo "Reset a case after a run with: git -C <case> reset --hard && git -C <case> clean -fd"
