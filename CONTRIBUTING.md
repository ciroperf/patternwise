# Contributing

Thanks for helping make patternwise more accurate. The most useful contributions, in order:

## 1. Wrong or missed findings

A false positive, a missed smell, a pattern verdict that is wrong, or a suggestion that adds
machinery without paying off. [Open a "wrong finding" issue](https://github.com/ciroperf/patternwise/issues/new?template=wrong-finding.yml)
with the report row, the agent and model, and a minimal snippet (or a public repo + commit).

Confirmed reports become regression cases in [`evals/cases/`](evals/cases/) with an answer key
in [`evals/expected/`](evals/expected/). A PR that adds the case together with the skill fix is
the best kind.

## 2. Knowledge base

The references in [`skills/patternwise/references/`](skills/patternwise/references/) are loaded
on demand, one file at a time, so each file must stand on its own. When you change one:

- write it in your own words: never copy text from the source books or refactoring.guru;
- keep the existing shape (recognition cues, misuse signs, when to ignore, treatments);
- add per-language idioms to `language-idioms.md`, not inside every pattern file;
- check that every `references/...` path you mention exists (CI checks this too).

## 3. The skill workflow

[`SKILL.md`](skills/patternwise/SKILL.md) stays short: workflow, severity rubric, report
template and safety rules. Detail belongs in `references/`. The safety rules (no edits before
an approved plan, tests after every step, no edits when tests cannot run) are not up for
loosening.

Any behavior change needs at least the `py-orders` case from [`evals/`](evals/) run and
compared with `evals/expected/py-orders.md`. Changes to Fix mode need `js-notify` too. Put the
result in the PR description and in the changelog entry.

## 4. The hotspot scanner

[`scripts/hotspots.py`](skills/patternwise/scripts/hotspots.py) is stdlib-only Python 3.8+.
No dependencies, ever. If you change it, update the bash/PowerShell fallback in
`references/no-python-fallback.md` when the output changes meaning.

## Pull requests

- Run the checks CI runs:

  ```bash
  python skills/patternwise/scripts/hotspots.py --selftest
  ```

- Keep everything in English.
- One topic per PR.
- Add a line to [CHANGELOG.md](CHANGELOG.md) under **Unreleased**.

[AGENTS.md](AGENTS.md) has the same rules in short form for coding agents working on the repo.

## Releases (maintainer)

Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` together, turn
**Unreleased** into `## X.Y.Z - YYYY-MM-DD` in the changelog, commit, then:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z" && git push origin vX.Y.Z
```

The release workflow checks that the tag matches both manifests and publishes
`patternwise-vX.Y.Z.zip` with the changelog section as release notes.
