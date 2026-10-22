# Working on this repo

- The skill is `skills/patternwise/`. Everything else (evals, manifests, docs) is not installed.
- `SKILL.md` stays short (workflow, rubric, report template). Detail goes in `references/`,
  which the agent loads on demand: keep each reference file self-contained.
- Skill text is English. Do not copy text from the source books: rewrite.
- `scripts/hotspots.py` is stdlib-only Python 3.8+. Run `python skills/patternwise/scripts/hotspots.py --selftest` after changes.
- Any behavior change to the skill: run at least the `py-orders` case from `evals/` and compare with
  `evals/expected/py-orders.md`. Note the result in `CHANGELOG.md`.
- Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` together.
