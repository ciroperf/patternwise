---
name: patternwise
description: Analyze, critique and refactor an existing codebase with design patterns and code smells. Invoked explicitly as a command with a mode (analyze, suggest or fix) and an optional path. Fix always shows a plan and waits for approval before editing, then works step by step with tests.
argument-hint: "[analyze|suggest|fix] [path]"
disable-model-invocation: true
---

# patternwise

Diagnose and treat object/module design problems in an existing codebase. Reason in
**cause → remedy chains**: a concrete *smell* (symptom) points to a *refactoring technique*
(treatment), which sometimes converges on a *design pattern* (target structure).

A pattern is never the goal. The goal is code that is easier to change. Recommend a pattern
only when it removes a problem that exists **today** in this code.

**Non-negotiables** (check before you answer):
1. Map before judging: run `scripts/hotspots.py`; if no Python works, run the commands in
   `references/no-python-fallback.md`. Never skip mapping.
2. Use the report template in step 4: tables, a `file:line` and a severity on every finding.
3. One verdict per pattern occurrence.
4. Never edit files before the user approves a plan, even for a "simplify" request that looks
   obvious and even if another refactoring workflow also applies. A request to refactor is
   a request for a plan first.
5. Fix mode: run the tests before the first edit and after every step, without being asked.
   If they cannot run (missing interpreter, sandbox), say so and do not edit: ask the user to
   run them or to enable them. If there are no tests, the first plan step is
   characterization tests.

## Modes

This skill runs only when the user invokes it: `/patternwise <mode> [path] [notes]` in Claude
Code, `$patternwise <mode> [path] [notes]` in Codex. The first word of the arguments picks the
mode; the rest is the perimeter and any extra instructions.

| Command | Mode | Edits code? |
|---------|------|-------------|
| `analyze [path]` | **Analyze**: patterns present with verdicts, code smells, report | No |
| `suggest [path]` | **Suggest**: Analyze + opportunities, each justified by a problem today | No |
| `fix [path]` | **Fix**: Analyze + Suggest + plan, then apply only the approved steps | Yes, only after the user approves a plan |

- No mode word (only a path, or nothing): run **Analyze** and offer `suggest` and `fix` at
  the end.
- Accept the Italian aliases `analizza`, `suggerisci`, `sistema` and obvious synonyms
  (`review` = analyze, `refactor` = fix). If the first word is something else, treat the
  whole argument as the request and pick the closest mode, saying which one you picked.
- Never escalate on your own: an `analyze` or `suggest` run does not edit, even if the user
  wrote "and fix it" in the notes; offer `fix` instead.

Modes are cumulative: Suggest includes a (lighter) Analyze; Fix includes Analyze + Suggest +
an approved plan.

## Scope

- Establish the perimeter first: a file, a module/package, or the whole repo. The path argument
  sets it. If there is none, use what the user pointed at (open file, mentioned path); otherwise ask once.
- Never edit anything outside the perimeter. If a fix needs changes outside it (e.g. callers
  in another module), list them in the plan as "outside scope" and ask.
- Exclude generated code, vendored dependencies, build output, migrations and lockfiles from
  analysis unless explicitly requested.

## Workflow

### 1. Recognize the project

- Identify languages, frameworks, build tool, test runner, linters, and how to run them
  (look at manifests: `package.json`, `pyproject.toml`, `pom.xml`, `build.gradle`,
  `*.csproj`, `go.mod`, `Cargo.toml`, `Makefile`, CI config).
- Note house conventions: naming, folder layout, DI style, error handling, functional vs OO.
- Load `references/language-idioms.md` and adapt every pattern to the language's idioms
  (in Python/JS/Kotlin/Go a Strategy is often just a function; a Singleton is often a module).
- Respect the existing architecture (layers, hexagonal, MVC, framework conventions). Do not
  propose moving the project to a different architecture unless asked.

### 2. Map the structure

- Run `python scripts/hotspots.py <path>` (stdlib only; `--help` for options) to get large
  files, churn × size hotspots, suspicious names, conditional density and repeated type-code
  comparisons (same attribute tested against several literals, possibly across files — the
  main lead for Switch Statements). Treat its output as leads, not verdicts. Try `python`,
  then `python3`, then `py -3` (sandboxed shells on Windows often lack `python`). If none
  runs, do not skip this step: use the bash or PowerShell commands in
  `references/no-python-fallback.md` (churn, size, repeated type-code comparisons).
- Read the hotspot files and their main collaborators. Build a mental map: modules, who
  depends on whom, where responsibilities live, where logic is duplicated.
- Read before judging. Never report a smell or pattern in code you have not opened.

### 3. Diagnose

For each finding gather: **location** (`path:line-range`), **evidence** (what in the code shows
it), **impact** (what change it makes hard or risky), **severity**, **remedy**.

- **Smells**: check the code against `references/smells.md`. Each smell entry lists the
  refactorings that treat it and when to ignore it.
- **Patterns present**: use `references/patterns/index.md` to recognize candidates by
  structure (roles and relationships), not by names. Then open the specific pattern file and
  classify each occurrence with exactly one verdict (pick the dominant one, explain nuances
  in the evidence column):
  - **Sound** – intent, structure and trade-off all fit the problem.
  - **Misapplied** – real pattern structure but wrong problem, broken roles, or leaking
    abstraction (e.g. Singleton used as global mutable state; Observer with ordering
    assumptions; Visitor over a hierarchy that changes often).
  - **Name only** – called `*Factory`, `*Manager`, `*Strategy`, `*Adapter`... without the
    structure (e.g. a "Factory" that is a static helper returning one concrete type).
    Not a bug by itself; report it only if the name misleads or hides a smell (God object,
    Middle Man, Data Class).
  - **Over-engineered** – pattern machinery with a single variant, no variation in sight,
    or indirection nobody needs (interface with one implementation and no test seam,
    factory for one product, Strategy with one strategy). Recommend simplification.
  - **Uncertain** – say so explicitly and state what evidence would settle it. Never force
    a label.

  The patterns table lists catalog patterns (GoF and well-known ones like Repository,
  Middleware, Plugin registry). Vague role names (`*Manager`, `*Processor`, `*Service`,
  `*Helper`) are not patterns: if they hide a problem, report it as a smell (Large Class,
  Long Method, Middle Man).
- **Opportunities** (Suggest/Fix): follow `references/chains.md` from the smell to the
  technique to a pattern. Propose a pattern only when you can name the concrete problem it
  fixes, in this code, now (a switch duplicated in 3 places, a class that changes for 4
  different reasons...). Otherwise propose the plain refactoring and stop there.

Severity rubric:

| Severity | Meaning |
|----------|---------|
| **High** | Causes or will plausibly cause bugs, blocks frequent changes, or forces shotgun edits on a hot path (high churn). Fix first. |
| **Medium** | Real maintenance cost, localized; fix when touching the area. |
| **Low** | Cosmetic or theoretical; mention briefly, often "leave as is". |

Weigh severity by churn: a smelly file nobody touched in two years is usually Low. A
conditional on the same type code repeated in 3+ places of the same class or module is High
by default: every new type is a shotgun edit. The same vocabulary translated once per
polymorphic implementation (one branch set per backend/adapter) is not that smell.

### 4. Report

Use this structure (keep it in the user's language; code identifiers stay as they are):

```markdown
# patternwise report – <scope>

## Context
Language/framework, test command, perimeter, what was excluded, coverage of the analysis.

## Summary
3–6 bullets: the biggest risks and the best-value changes.

## Patterns found
| Pattern | Where | Verdict | Evidence / note |
|---|---|---|---|
| Strategy | src/pricing/rules.py:10-80 | Sound | ... |
| "PaymentFactory" | src/pay/factory.ts:1-40 | Name only | static helper, one product |

## Code smells
| # | Smell (family) | Where | Severity | Evidence | Recommended technique |
|---|---|---|---|---|---|

## Opportunities
For each: problem today → technique(s) → target structure (pattern or not) → expected gain → cost/risk.

## Over-engineering to simplify
## Open questions / uncertainties
```

Order findings by severity, then by churn. Group repeats of the same smell instead of listing
each instance. Point to `file:line` for every claim, citing only lines you have read.
Keep the smells table to findings that matter; collapse Low ones into a single "Minor" bullet
list so the report stays proportional to the code (a 100-line module does not need 13 rows).
Bugs found along the way go in their own "Bugs (behavior changes, not refactorings)" list.

In Analyze/Suggest mode stop after the report and offer the next command (`suggest`, `fix`).

### 5. Plan (Fix mode) – ask before editing

Present a numbered refactoring plan and **wait for explicit approval** before modifying any
file. Each step:

- technique from the catalog (e.g. "Extract Method", "Replace Conditional with Polymorphism");
- files and symbols touched; whether public API changes;
- why (which finding it resolves);
- risk (Low/Med/High) and how it will be verified.

Rules for the plan:
- Order: safety net first (characterization tests), then low-risk local moves (Extract
  Method, Rename, Extract Variable), then moves between classes, then hierarchy/pattern
  changes. Each step must leave the code compiling and tests green.
- Prefer many small steps over one big rewrite. Mark any step that is not a pure refactoring
  (behavior change, bug fix) as such and keep it separate.
- If there are no tests, say so and propose characterization tests before every Medium/High
  risk step (see `references/refactoring-safety.md`).
- The user may approve all, some, or reorder. Do only what was approved.

### 6. Apply (Fix mode)

For each approved step:
1. Open the technique's entry in `references/refactorings/<group>.md` and follow its mechanics.
2. Make the smallest change that completes the step; preserve observable behavior
   (outputs, side effects, exceptions, public signatures unless the step says otherwise).
3. Run build/type-check/tests (the commands found in step 1). If they fail, fix forward only
   if the cause is obvious and inside the step; otherwise revert the step and report.
4. Briefly log: step, files, result of verification.

Do not combine steps, do not "also tidy" unrelated code, do not reformat whole files, do not
rename things the plan did not mention. If a new problem appears, add it to the remaining
work list instead of fixing it on the spot. If you use version control, suggest one commit
per step (do not commit unless the user asks).

### 7. Close

Summarize: steps done (with verification result), files changed, behavior changes (should
be none, or explicitly approved ones), what remains from the report, and suggested next steps.
State clearly anything not verified (e.g. no tests covered module X).

## What counts as a refactoring here

A refactoring **preserves observable behavior**, follows a **named technique** from the catalog,
and proceeds in **small verifiable steps**. It may reshape hierarchies, dependencies and
responsibilities to reach a pattern. Renaming a class or moving a file, alone, is not the
point; do it only when it is a step of a technique (e.g. Rename Method to reveal intent,
Move Method to fix Feature Envy).

## Principles

- **YAGNI / KISS**: no speculative variation points. A pattern must pay for its indirection
  today. Flag over-engineering with the same seriousness as smells.
- **Fit the codebase**: follow existing style, naming, layering and libraries. Use the
  framework's own mechanisms (DI container, middleware, signals/events) instead of hand-made
  pattern code when they exist.
- **Evidence over labels**: cite code. When unsure, say "possibly X, because ..., would need
  Y to confirm".
- **Smallest effective treatment**: often Extract Method / Move Method fixes the problem and
  no pattern is needed.
- **Behavior is sacred**: if a change can alter behavior, it is not a refactoring step; isolate
  it and ask.

## Reference map (load only what you need)

Start with `smells.md`, `patterns/index.md` and `language-idioms.md`. Open any other file only
when a specific finding needs it (one pattern file per pattern judged, one refactoring group
per technique proposed). Never bulk-read the `references/` tree: it wastes context on large
codebases.

| File | Load when |
|------|-----------|
| `references/smells.md` | Diagnosing smells (all modes) |
| `references/chains.md` | Going from a finding to a remedy (Suggest/Fix) |
| `references/patterns/index.md` | Recognizing patterns; deciding which pattern file to open |
| `references/patterns/<category>/<pattern>.md` | Judging or introducing a specific pattern |
| `references/refactorings/composing-methods.md` | Long methods, temps, unclear expressions |
| `references/refactorings/moving-features.md` | Responsibilities in the wrong class |
| `references/refactorings/organizing-data.md` | Primitives, type codes, encapsulation, magic numbers |
| `references/refactorings/simplifying-conditionals.md` | Complex/duplicated conditionals, nulls |
| `references/refactorings/simplifying-method-calls.md` | Signatures, parameters, queries vs commands, errors |
| `references/refactorings/dealing-with-generalization.md` | Inheritance, interfaces, delegation |
| `references/principles.md` | Justifying a recommendation (SOLID, composition, coupling) |
| `references/language-idioms.md` | Adapting patterns/techniques to the project's language |
| `references/refactoring-safety.md` | No/weak tests, risky steps, verification commands |
