# Evaluating patternwise

Three hand-built cases with answer keys, plus a citation checker for runs on real codebases.

## Setup

```bash
bash evals/setup.sh
```

Creates `../patternwise-sandbox/{py-orders,js-notify,py-legacy-docs}`, each its own git repo.
The answer keys in `expected/` are not copied, so the agent cannot see them.

| Case | Language | Tests | What it measures |
|---|---|---|---|
| `py-orders` | Python | `python -m unittest discover -s tests -t .` | classic smells, misused Singleton, name-only Factory, refactoring towards Strategy |
| `js-notify` | Node ESM | `npm test` | recognizing a sound Strategy and **over-engineering** without inventing patterns |
| `py-legacy-docs` | Python | none | discipline: characterization tests before any edit; State and Template Method opportunities |

## Prompts

Open the agent inside a case folder and run, in order (Claude Code shown; in Codex use
`$patternwise` instead of `/patternwise`):

1. `/patternwise analyze`
2. `/patternwise suggest`
3. `/patternwise fix shop/orders.py` (`js-notify`: `/patternwise fix src/`;
   `py-legacy-docs`: `/patternwise fix docs/document.py`)

The skill is explicit-only. Also check the negative case: a plain "refactor this" prompt must
not load it.

Headless:

```bash
claude -p "<prompt>" --allowedTools "Bash Read Grep Glob Skill" --disallowedTools "Edit Write NotebookEdit"
```

```bash
codex exec -s read-only -o report.md "<prompt>"
```

On Git Bash (Windows) set `MSYS_NO_PATHCONV=1`, otherwise `/patternwise` is rewritten into a
Windows path before it reaches the agent. In Codex, escape the dollar sign: `"\$patternwise ..."`.

## Scoring

Compare with `expected/<case>.md`. Checklist:

- [ ] The command picks the right mode; `analyze` and `suggest` never edit.
- [ ] Every finding has file:lines, severity, evidence and a catalog technique.
- [ ] Each pattern gets exactly one verdict: sound / misapplied / name only / over-engineered / uncertain.
- [ ] Fix mode presents a plan and **waits for approval** before editing.
- [ ] Tests run before and after each step; `py-legacy-docs` gets characterization tests first.
- [ ] Behavior unchanged (`git diff` + green tests); nothing edited outside scope.

On real repositories (no key), check that every citation and identifier exists:

```bash
python evals/check_refs.py report.md path/to/repo
```

Reset a case: `git -C ../patternwise-sandbox/<case> reset --hard && git -C ../patternwise-sandbox/<case> clean -fd`
