<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/banner-light.svg">
  <img alt="patternwise: design patterns and refactoring, only where they pay off" src="assets/banner-light.svg" width="100%">
</picture>

<br/>

**An agent skill that reviews your design like a senior engineer: it finds code smells, judges the
patterns already in your code, and refactors in small tested steps, only after you approve the plan.**

[![License: MIT](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-7c3aed.svg)](skills/patternwise/SKILL.md)
[![Release](https://img.shields.io/github/v/release/ciroperf/patternwise?color=blue)](https://github.com/ciroperf/patternwise/releases/latest)
[![CI](https://github.com/ciroperf/patternwise/actions/workflows/ci.yml/badge.svg)](https://github.com/ciroperf/patternwise/actions/workflows/ci.yml)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-supported-D97757?logo=claude&logoColor=white)](#install)
[![Codex](https://img.shields.io/badge/Codex-supported-111111)](#install)
[![Any SKILL.md agent](https://img.shields.io/badge/Cursor%20%C2%B7%20Copilot%20%C2%B7%20Antigravity-via%20skills.sh-555555)](#install)

```bash
npx skills@latest add ciroperf/patternwise
```

[Why](#why) · [What you get](#what-you-get) · [Commands](#three-commands) · [Install](#install) · [How it works](#how-it-works) · [Tested](#tested-not-vibed) · [Contributing](#contributing)

</div>

---

## Why

Ask a coding agent to "refactor with design patterns" and you usually get one of two things:

- **Pattern cosplay**: an `AbstractNotifierFactory`, an `INotifier` with one implementation, an
  event bus between two functions. More files, same problems.
- **Vague advice**: "consider applying SOLID principles", with no line numbers and no plan.

patternwise makes the agent reason the way the refactoring literature does, from a concrete
symptom to the smallest treatment that fixes it:

```
 code smell  ──▶  refactoring technique  ──▶  design pattern (only if it fixes a problem you have today)
 "switch on customer_type    "Replace Conditional       Strategy, as a dict of functions
  repeated in 3 places"       with Polymorphism"         (idiomatic Python, not a class zoo)
```

## What you get

- ⚖️ **A verdict on every pattern, not just a name.** Sound, misapplied, name only,
  over-engineered or uncertain, with the evidence.
- 📍 **Evidence, not opinion.** Every finding has `file:line`, a severity weighted by git churn,
  the change it makes hard, and a named technique from a catalog of 66 refactorings.
- ✂️ **It deletes as readily as it adds.** Over-engineering is reported as seriously as smells:
  Remove Middle Man and Collapse Hierarchy are first-class remedies.
- 🛡️ **It never edits without asking.** Fix mode shows a numbered plan, waits for your approval,
  runs your tests after every step, and writes characterization tests first when there are none.
- 🐛 **Bugs are reported, not silently "fixed".** A refactoring keeps behavior identical; a bug
  it finds goes in its own list.
- 🌍 **Idiomatic in your language.** A Strategy in Python or JS is often just a function, a
  Singleton is often a module. It follows your codebase's style, not a textbook's.

| Verdict | Meaning |
|---|---|
| ✅ **Sound** | Intent, structure and trade-off fit the problem |
| ⚠️ **Misapplied** | Real structure, wrong problem: e.g. a Singleton used as global mutable state |
| 🏷️ **Name only** | Called `*Factory` / `*Manager` / `*Proxy` without the structure |
| 🧱 **Over-engineered** | Machinery with one variant: interface with one impl, factory for one product |
| ❓ **Uncertain** | Says so, and says what evidence would settle it |

### Example (real output, trimmed)

> **Patterns found**
>
> | Pattern | Where | Verdict | Evidence |
> |---|---|---|---|
> | Singleton | `shop/config.py:1` | ⚠️ Misapplied | `get_instance()` exposes mutable global state (`orders_count`); the constructor is still public |
> | "PaymentFactory" | `shop/payments.py:9` | 🏷️ Name only | `create()` always returns `CardPayment`: one product, no creation decision |
>
> **Code smells**
>
> | Smell | Where | Severity | Remedy |
> |---|---|---|---|
> | Long Method | `OrderProcessor.process` (`orders.py:19`) | High | Extract Method per phase: validation, totals, invoice |
> | Repeated switch on `customer_type` | `shop/orders.py:35, 54, 106` | Medium | Centralize the rules first; Strategy only if the variants keep growing |

## Three commands

patternwise never runs on its own: you call it, and you pick the mode.

| Claude Code | Codex | What it does | Edits code? |
|---|---|---|---|
| `/patternwise analyze src/` | `$patternwise analyze src/` | Pattern verdicts + code smells report | No |
| `/patternwise suggest src/` | `$patternwise suggest src/` | Analyze + where a pattern or refactoring pays off | No |
| `/patternwise fix shop/orders.py` | `$patternwise fix shop/orders.py` | Plan, your approval, then small steps with tests | Only after you approve the plan |

The path is optional, and anything after it is passed along as notes
(`/patternwise fix src/ keep the public API`). No mode means `analyze`. In Codex you can also
pick it from the `/skills` menu. Italian aliases work too: `analizza`, `suggerisci`, `sistema`.

**Why explicit?** A refactoring workflow should start when you ask for it, not because a prompt
happened to say "clean up". In our tests implicit triggering was the least reliable part:
another installed skill could win the match and edit without a plan.

## Install

<details open>
<summary><strong>Any agent</strong> (Claude Code, Codex, Cursor, Copilot, Antigravity and more, via <a href="https://skills.sh">skills.sh</a>)</summary>

```bash
npx skills@latest add ciroperf/patternwise
```

Pick your agents interactively, or go non-interactive (`-g` = for your user, all projects):

```bash
npx skills@latest add ciroperf/patternwise -a claude-code -g
```

```bash
npx skills@latest add ciroperf/patternwise -a codex -g
```

</details>

<details>
<summary><strong>Claude Code plugin</strong> (auto-updates)</summary>

```
/plugin marketplace add ciroperf/patternwise
/plugin install patternwise@patternwise
```

</details>

<details>
<summary><strong>Codex plugin</strong></summary>

```bash
codex plugin marketplace add ciroperf/patternwise
```

```bash
codex plugin add patternwise@patternwise
```

</details>

<details>
<summary><strong>Manual</strong></summary>

Download `patternwise-vX.Y.Z.zip` from the [latest release](https://github.com/ciroperf/patternwise/releases/latest)
(or clone the repo) and copy [`skills/patternwise/`](skills/patternwise) into `~/.claude/skills/`
(Claude Code), `~/.agents/skills/` (Codex), or a single repo's `.claude/skills/`.

</details>

Optional: Python 3 for the hotspot scanner. Without it the skill falls back to git and ripgrep,
or plain bash/PowerShell.

## How it works

```mermaid
flowchart LR
  A[Recognize project<br/>stack, tests, idioms] --> B[Map hotspots<br/>churn × size, type codes]
  B --> C[Diagnose<br/>smells + pattern verdicts]
  C --> D[Report<br/>file:line, severity, remedy]
  D -->|Fix mode| E[Plan<br/>waits for approval]
  E --> F[Apply one step<br/>run tests]
  F -->|next step| F
  F --> G[Close<br/>summary, what is left]
```

Under the hood:

- **[`SKILL.md`](skills/patternwise/SKILL.md)**: the workflow, severity rubric, report template
  and safety rules, under 300 lines.
- **[`references/`](skills/patternwise/references)**: loaded on demand, one file per finding,
  never all at once.
  - 23 code smells, each with treatments and when to ignore it.
  - Smell → technique → pattern chains.
  - 66 refactoring techniques with their mechanics.
  - All 22 GoF patterns with recognition cues, misuse signs and per-language idioms.
- **[`scripts/hotspots.py`](skills/patternwise/scripts/hotspots.py)**: a zero-dependency
  scanner for the largest and most-changed files, dense conditionals, and the same attribute
  compared against many literals across files (the main lead for Switch Statements). About
  10 s on Django's 124k lines.

## Tested, not vibed

The repo ships with [hand-built cases and answer keys](evals) and a citation checker that
flags any `file:line` or identifier the agent made up.

| Run | Claude Code | Codex |
|---|---|---|
| `py-orders` vs answer key | 2/2 pattern verdicts · **8/8 smells** · found and reproduced a real pricing bug | 2/2 pattern verdicts · 6/8 smells |
| Fix mode, 3 eval rounds | `py-orders`, `py-legacy-docs`, `js-notify`: plan first, edits only after approval, tests up (6→16, 0→22) and green after every step, outputs unchanged, bug reported instead of "fixed" | `js-notify`: plan first, 3 steps, 5/5 green after each. When its sandbox could not run the tests, it refused to edit, every time |
| axios `lib/`, httpie, Django `db/backends` | 104 citations, 1 off-by-one line range, 0 invented files | 64 citations, **0 invented** |
| Real issues surfaced | httpie: shared mutable `env=Environment()` default in 5 places | httpie: plugin registry re-registers on every load |

Every finding quoted above was checked by hand against the code. Every run on a real
repository fed something back into the skill: fallbacks for sandboxes without Python or
ripgrep, test-noise filtering in the scanner, one verdict per pattern, and reports that stay
proportional to the code.

## Principles

**YAGNI / KISS** · **fit the codebase's existing style** · **evidence over labels** ·
**smallest effective treatment** · **behavior is sacred**

## Contributing

Found a false positive, a missed smell, or a suggestion that does not pay off?
[Open a "wrong finding" issue](https://github.com/ciroperf/patternwise/issues/new?template=wrong-finding.yml)
with the report row and a minimal snippet: each confirmed one becomes a regression case in
`evals/`. Knowledge-base fixes, new language idioms and eval cases are all welcome. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Contributors

<a href="https://github.com/ciroperf/patternwise/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ciroperf/patternwise" alt="patternwise contributors" />
</a>

Created and maintained by [@ciroperf](https://github.com/ciroperf). Every merged PR and every
confirmed "wrong finding" report earns a spot here.

## Credits

The knowledge base is distilled and rewritten from Alexander Shvets' *Dive Into Design Patterns*
and *Dive Into Refactoring* and the [refactoring.guru](https://refactoring.guru) taxonomy. No
text from those works is reproduced. Buy the books, they are excellent.

## License

[MIT](LICENSE) © ciroperf
