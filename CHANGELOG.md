# Changelog

## 0.1.0

First public release.

- Three explicit commands: `/patternwise analyze|suggest|fix [path]` in Claude Code,
  `$patternwise ...` in Codex. The skill never loads on its own
  (`disable-model-invocation: true`, `agents/openai.yaml` with `allow_implicit_invocation: false`).
- Fix: plan + approval + tests after every step.
- Knowledge base: 23 smells, smell → technique → pattern chains, 66 refactoring techniques,
  22 GoF patterns with misuse signs, language idioms, refactoring safety rules.
- `scripts/hotspots.py`: churn × size, conditional density, repeated type-code comparisons,
  pattern-ish names; skips tests and vendored code; `--selftest`.
- Evals: three cases with answer keys and `evals/check_refs.py` (flags invented citations).
- Hardened on real codebases (axios, httpie, Django) with Claude Code and Codex:
  - bash/PowerShell fallbacks for sandboxes without Python or ripgrep;
  - `git safe.directory` for sandboxes running as another user;
  - one verdict per pattern;
  - vague role names reported as smells, not as patterns;
  - Low findings collapsed and bugs listed separately;
  - references loaded on demand.
