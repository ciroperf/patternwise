# Refactoring safely

## The contract
- Observable behavior stays identical: return values, outputs, side effects (I/O, DB writes,
  events, logs if they are consumed), exceptions and their types, performance characteristics
  that matter, public signatures (unless the plan explicitly changes an API and updates all
  callers in scope).
- Every step leaves the build green and the tests passing. If a step cannot be finished
  safely, revert it rather than leave a half state.
- Refactoring and behavior change never share a step.

## Before starting
1. Find the verification commands: test runner, type checker/compiler, linter, build.
   Look at CI config, `Makefile`, package scripts, README, contributing docs.
2. Run them once **before** any edit and record the baseline. Pre-existing failures are not
   yours: report them and do not "fix" them silently.
3. Check coverage of the code you will touch (run coverage if available, or read tests).

## No or weak tests
Say so in the report and the plan. Before any Medium/High-risk step propose
**characterization tests**:
- Pin current behavior, not intended behavior (bugs included — note them separately).
- Drive the code through its public entry point with representative inputs; capture outputs
  and side effects (golden master/snapshot or approval testing for complex outputs).
- Cover each branch you will move (conditionals being replaced by polymorphism, each type
  code value, null/empty cases, error paths).
- Non-determinism (current date/time, random, UUIDs, environment, ordering of sets/dicts from
  I/O): pin it — inject the value, patch it with the framework's mocking tool, or assert on a
  pattern instead of the exact value. Flag it in the report; it is often a missing seam.
- Use the project's existing test framework and layout; do not add a new framework without
  approval.
- The new tests must run with the project's test command, not only when called by name. If
  the project has no command yet, make the tests run with the framework's zero-argument
  default, the command a newcomer would try without reading your notes: `python -m unittest`
  (needs `tests/__init__.py` and `test_*.py` names), `pytest`, `npm test`, `go test ./...`.
  State that command in the plan and use it for every later step.
- Prove it: run the command before and after adding the tests and report both test counts.
  If the count did not go up, the tests are not collected; fix that before refactoring.
- Seams: if the code is untestable (static calls, `new` of infrastructure, global state),
  introduce the minimum seam first (Extract Method + parameterize, pass a dependency in,
  wrap the static call) and treat that as a step of the plan.

If the user declines tests, restrict yourself to low-risk, mechanical steps (Extract Variable,
Extract Method within one function, Rename with all references updated by tooling) and say so.

## Risk rating per step
- **Low**: local, mechanical, tool-supported (Rename via LSP/IDE, Extract Variable, Extract
  Method in one file, Inline Temp, Replace Magic Number).
- **Medium**: moves across classes/files (Move Method/Field, Extract Class, Introduce Parameter
  Object, Encapsulate Collection), signature changes with many callers.
- **High**: hierarchy and dispatch changes (Replace Conditional with Polymorphism, Replace
  Inheritance with Delegation, Replace Type Code with State/Strategy, introducing a pattern
  across modules), anything touching concurrency, serialization, persistence mappings,
  reflection, DI configuration, or public APIs.

## Hazards to check before each step
- Reflection, string-based lookups, serialization field names, ORM mappings, DI wiring by
  name/type, templates referring to members, public API consumers outside the repo.
- Equality/hash semantics when turning references into values (or vice versa).
- Mutability: extracting shared state, aliasing, defensive copies when encapsulating
  collections.
- Evaluation order and short-circuiting when restructuring conditionals.
- Exceptions: moved code may change which exception is thrown or where it is caught.
- Concurrency: locks, thread-confinement, async boundaries.
- Overload resolution and virtual dispatch after moving or renaming methods.

## Executing
- Use the language server / IDE refactoring tools when available (rename, extract, move) —
  they update references precisely.
- After each step: compile/type-check, then run the relevant tests (fast subset first, full
  suite at the end and at checkpoints).
- Keep a per-step log: technique, files, verification command + result.
- Suggest one commit per step when under version control (only commit if asked).
