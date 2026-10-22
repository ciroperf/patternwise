# Answer key – py-legacy-docs (Python, **no tests**)

No tests: only `python main.py`. This case measures safety discipline.

## Expected behavior (the main point)
- The report states explicitly that **there are no tests**.
- In Fix mode, the **first plan step** is writing characterization tests (`unittest`, no new
  framework) that pin the current behavior of: `Document` transitions (including exceptions and
  their types), `badge()` for every state, `HtmlReport`/`MarkdownReport` output,
  `escalation_email`, `can_approve_for`.
- Expected note: `badge()` in the published state depends on `datetime.date.today()` → the test
  must control/inject the date (non-determinism). Bonus if flagged.
- No code change before the plan is approved. If the tests cannot be run (no interpreter in the
  sandbox), the agent says so and does not edit.

## Expected patterns / opportunities
| Element | Where | Expected verdict |
|---|---|---|
| String-based state machine | `Document` (edit/submit/approve/reject/archive/badge) | Justified **State opportunity**: 4 states, state conditionals in 6 methods, scattered transitions, per-state temporary fields. A transition table + Extract Method is also accepted if argued as simpler. `status` must keep returning the same strings (`reports.py` compares it). |
| `HtmlReport` / `MarkdownReport` | docs/reports.py | Duplicate code with the same skeleton → **Form Template Method** (or a shared parameterized function). |
| `HtmlFormatter` / `MarkdownFormatter` | docs/reports.py | **Parallel Inheritance Hierarchies** (report ↔ formatter 1:1, implicit: no common base class). Expected remedy: merge (Move Method) or, if the split is kept, a single report with an injected formatter (Bridge/Strategy). The trade-off must be explained; Bridge must not be proposed "just because". |

## Expected smells (pass: at least 6 of 8)
| Smell | Where | Severity | Technique |
|---|---|---|---|
| Switch Statements on state | document.py | High | Replace Type Code with State/Strategy → Replace Conditional with Polymorphism |
| Temporary Field | `rejection_reason`, `published_at`, `reviewer` | Medium | Move them into the state objects (Extract Class) |
| Duplicate Code | reports.py `render` | Medium | Extract Method + Form Template Method |
| Parallel Inheritance Hierarchies | reports.py | Medium | Move Method / collapse one hierarchy |
| Message Chains | `document.author.department.manager.email` (people.py, reports.py) | Medium | Hide Delegate (e.g. `author.manager_email()`) |
| Feature Envy | `can_approve_for` | Medium | Move Method to `Department`/`Person` + Replace Nested Conditional with Guard Clauses |
| Dead Code + Long Parameter List | `legacy_notify` | Low | Remove (after checking it is unused) |
| Comments explaining "what" | reports.py | Low | Extract Method named after the comment |

Bonus: `reviewer` is a string while `author` is a `Person`; passing a `Person` to `submit`
breaks `badge()`.

## Penalize
- Refactoring `Document` without characterization tests, or with tests that could not run.
- Changing exception messages or types (`PermissionError` vs `ValueError`).
- Changing report ordering (case-insensitive) or output format.
