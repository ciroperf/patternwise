#!/usr/bin/env python3
"""Map structural hotspots of a codebase (stdlib only).

Prints a Markdown report: largest files, churn x size hotspots (if git is available),
suspicious names (Manager/Factory/Helper...), conditional density (switch/elif/instanceof), and
attributes repeatedly compared against literals/constants (type codes, across files).
Output is a list of leads for the agent to read, not a verdict.

Test files/dirs and .d.ts declarations are skipped unless --include-tests.

Usage: python hotspots.py [PATH] [--top N] [--since "12 months ago"] [--include-tests] [--selftest]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter

CODE_EXT = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".java", ".kt", ".kts", ".scala",
    ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".c", ".cc", ".cpp", ".h", ".hpp",
    ".m", ".dart", ".ex", ".exs", ".clj", ".fs", ".vue", ".svelte",
}
SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "out", "target", "bin", "obj",
    ".venv", "venv", "env", "__pycache__", ".idea", ".vscode", ".next", ".nuxt",
    "coverage", "migrations", "generated", ".gradle", "Pods", ".dart_tool",
}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "testing", "e2e", "fixtures"}
TEST_FILE = re.compile(r"(?:^test_.*\.py|_test\.\w+|\.(?:test|spec)\.\w+|Tests?\.\w+)$")
# Type declarations only (class-like keywords) named after a pattern role, or base classes.
SUSPICIOUS = re.compile(
    r"\b(?:class|interface|struct|object|trait)\s+((?:Abstract|Base)\w*|\w*(?:Manager|Helper|Util|"
    r"Utils|Factory|Singleton|Handler|Processor|Service|Controller|Adapter|Proxy|Wrapper|Strategy|"
    r"Builder|Visitor|Observer|Listener|Command|Facade|Mediator))\b"
)
CONDITIONAL = re.compile(r"\b(?:switch|case|elif|else\s+if|instanceof|isinstance|when|match)\b")
# `x.kind == "gold"`, `type === 'vip'`, `role == ROLE_ADMIN`, `s == Status.DRAFT`: a type code being branched on.
TYPE_CODE = re.compile(
    r"(?<![\w.])(?<!typeof )([A-Za-z_][\w.]*)\s*(?:===?|!==?)\s*"
    r"(\"[^\"\n]*\"|'[^'\n]*'|[A-Z][A-Z0-9_]+\b|[A-Z]\w*\.[A-Z][A-Z0-9_]*\b)"
)


def code_files(root, include_tests=False):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")
                   and (include_tests or x.lower() not in TEST_DIRS)]
        for f in files:
            if (os.path.splitext(f)[1].lower() in CODE_EXT and ".min." not in f
                    and not f.endswith(".d.ts") and (include_tests or not TEST_FILE.search(f))):
                yield os.path.join(d, f)


def scan(path):
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    loc = sum(1 for line in text.splitlines() if line.strip())
    # key by the last name segment so `self.kind` and `customer.kind` count together
    codes = [(subject.rsplit(".", 1)[-1], value) for subject, value in TYPE_CODE.findall(text)]
    return loc, len(CONDITIONAL.findall(text)), sorted(set(SUSPICIOUS.findall(text))), codes


def git_churn(root, since):
    try:
        # safe.directory: sandboxed agents often run as a different user than the repo owner
        git = ["git", "-c", "safe.directory=*", "-C", root]
        top = subprocess.run([*git, "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True).stdout.strip()
        def log(*window):
            return subprocess.run([*git, "log", *window, "--name-only", "--format="],
                                  capture_output=True, text=True, check=True).stdout
        label, out = f"commits since {since}", log(f"--since={since}")
        if not out.strip():  # stale checkout: fall back to the most recent history
            label, out = "last 300 commits, none in the time window", log("-n", "300")
    except (OSError, subprocess.CalledProcessError):
        return None, None
    return label, Counter(os.path.normcase(os.path.normpath(os.path.join(top, p)))
                          for p in out.splitlines() if p.strip())


def report(root, top, since, include_tests=False):
    rows, type_codes = [], {}  # type_codes: attribute -> list of (file, compared value)
    for f in code_files(root, include_tests):
        loc, conds, names, codes = scan(f)
        rel = os.path.relpath(f, root)
        rows.append((rel, loc, conds, names, os.path.normcase(os.path.abspath(f))))
        for attr, value in codes:
            type_codes.setdefault(attr, []).append((rel, value))
    if not rows:
        return f"No source files found under {root}."
    churn_label, churn = git_churn(root, since)
    out = [f"# Hotspots for `{os.path.abspath(root)}`", "",
           f"{len(rows)} source files, {sum(r[1] for r in rows)} non-blank lines"
           + ("." if include_tests else " (tests excluded; --include-tests to add them)."), ""]

    out += ["## Largest files", "", "| File | LOC | Conditionals |", "|---|---|---|"]
    for rel, loc, conds, _, _ in sorted(rows, key=lambda r: -r[1])[:top]:
        out.append(f"| {rel} | {loc} | {conds} |")

    if churn:
        out += ["", f"## Churn x size ({churn_label})", "",
                "| File | Commits | LOC | Score |", "|---|---|---|---|"]
        scored = [(rel, churn.get(key, 0), loc) for rel, loc, _, _, key in rows]
        for rel, c, loc in sorted(scored, key=lambda r: -(r[1] * r[2]))[:top]:
            if c:
                out.append(f"| {rel} | {c} | {loc} | {c * loc} |")
    else:
        out += ["", "_No git history available: churn skipped._"]

    out += ["", "## Conditional density (per 100 LOC)", "", "| File | Conditionals | Density |",
            "|---|---|---|"]
    dense = [(rel, conds, 100 * conds / loc) for rel, loc, conds, _, _ in rows if loc >= 20 and conds]
    for rel, conds, dens in sorted(dense, key=lambda r: -r[2])[:top]:
        out.append(f"| {rel} | {conds} | {dens:.1f} |")

    out += ["", "## Repeated type-code comparisons (Switch Statements / State / Strategy candidates)", ""]
    repeated = [(attr, hits) for attr, hits in type_codes.items()
                if len(hits) >= 3 and len({v for _, v in hits}) >= 2]
    if repeated:
        out += ["| Attribute | Comparisons | Distinct values | Files |", "|---|---|---|---|"]
        for attr, hits in sorted(repeated, key=lambda r: -len(r[1]))[:top]:
            values = sorted({v for _, v in hits})
            files = Counter(rel for rel, _ in hits)
            out.append(f"| `{attr}` | {len(hits)} | {len(values)}: {', '.join(values[:6])} | "
                       + ", ".join(f"{rel} ({n})" for rel, n in files.most_common()) + " |")
    else:
        out.append("- none")

    out += ["", "## Pattern-ish or vague names (verify the structure, not the name)", ""]
    named = [(rel, n) for rel, _, _, names, _ in rows for n in names]
    out += [f"- `{n}` in {rel}" for rel, n in named[: top * 3]] or ["- none"]
    return "\n".join(out)


def selftest():
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "node_modules"))
        with open(os.path.join(d, "node_modules", "x.js"), "w") as fh:
            fh.write("class IgnoredManager {}\n")
        with open(os.path.join(d, "a.py"), "w") as fh:
            fh.write("class OrderManager:\n" + "    x = 1\n" * 25 + "if a:\n    pass\nelif b:\n    pass\n")
        with open(os.path.join(d, "b.js"), "w") as fh:
            fh.write('if (o.kind === "gold") a(); else if (o.kind === "vip") b();\n'
                     "if (n == 1 || n == 2 || n == 3) c();\n"  # numbers are not type codes
                     'if (env == "prod") d();\n'
                     "if (typeof Blob === 'undefined' || typeof Blob === 'function' || typeof Blob === 'x') e();\n"
                     "function setProxy() {}\n")
        with open(os.path.join(d, "c.py"), "w") as fh:
            fh.write('if self.kind == "gold":\n    pass\nif s == Status.DRAFT or s != Status.DONE:\n    pass\n')
        os.makedirs(os.path.join(d, "tests"))
        with open(os.path.join(d, "tests", "helpers.py"), "w") as fh:
            fh.write("class TestManager:\n    pass\n")
        with open(os.path.join(d, "x.spec.js"), "w") as fh:
            fh.write('if (o.kind === "a" || o.kind === "b" || o.kind === "c") f();\n')
        r = report(d, 10, "1 year ago")
        assert "a.py" in r and "OrderManager" in r, r
        assert "IgnoredManager" not in r and "TestManager" not in r, r  # vendored / test dirs
        assert "setProxy" not in r and "`Blob`" not in r, r  # functions, typeof checks
        assert "x.spec.js" in report(d, 10, "1 year ago", include_tests=True)
        assert '| `kind` | 3 | 2: "gold", "vip" | b.js (2), c.py (1) |' in r, r
        assert "`n`" not in r and "`env`" not in r, r  # numeric / single-value comparisons
        assert "`s`" not in r, r  # only 2 comparisons: below threshold
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--since", default="12 months ago")
    ap.add_argument("--include-tests", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    sys.stdout.reconfigure(encoding="utf-8")
    print(report(a.path, a.top, a.since, a.include_tests))


if __name__ == "__main__":
    main()
