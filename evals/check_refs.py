#!/usr/bin/env python3
"""Check a patternwise report against the repo it describes (stdlib only).

Flags `path:line` / `path:a-b` citations whose file is missing or whose lines are out of range,
and `backticked` identifiers that appear nowhere in the source files (likely hallucinated).

Usage: python check_refs.py REPORT.md REPO_DIR
"""
import os
import re
import sys

CITE = re.compile(r"((?:\b[A-Za-z]:)?[\w./\\-]+\.\w+):(\d+)(?:-(\d+))?")
IDENT = re.compile(r"`([A-Za-z_]\w{2,})(?:\(\))?`")


def main(report_path, repo):
    report = open(report_path, encoding="utf-8").read()
    files = {}
    for d, dirs, names in os.walk(repo):
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules"]
        for n in names:
            p = os.path.join(d, n)
            files[os.path.relpath(p, repo).replace("\\", "/")] = p

    def resolve(path):
        if os.path.isabs(path):  # agents often link absolute paths
            path = os.path.relpath(path, repo)
        path = path.replace("\\", "/").lstrip("./")
        if path in files and "/" in path:
            return [files[path]]
        # a bare or partial path (link text like `index.js:98`) may match several files
        return [p for rel, p in files.items()
                if ("/" + rel.lower()).endswith("/" + path.lower())]

    bad, cites = [], set(CITE.findall(report))
    for path, a, b in sorted(cites):
        candidates = resolve(path)
        if not candidates:
            bad.append(f"missing file: {path}")
            continue
        n = max(sum(1 for _ in open(f, encoding="utf-8", errors="ignore")) for f in candidates)
        if int(b or a) > n or int(a) < 1 or int(b or a) < int(a):
            bad.append(f"bad range: {path}:{a}{'-' + b if b else ''} (file has {n} lines)")

    text = "\n".join(open(p, encoding="utf-8", errors="ignore").read()
                     for rel, p in files.items() if os.path.splitext(rel)[1] in
                     {".py", ".js", ".ts", ".mjs", ".cjs", ".java", ".kt", ".cs", ".go", ".rb", ".php"})
    idents = set(IDENT.findall(report))
    unknown = sorted(i for i in idents if not re.search(r"\b" + re.escape(i) + r"\b", text))
    bad += [f"identifier not in source (fine if it is a proposed name): {i}" for i in unknown]

    print(f"{len(cites)} citations, {len(idents)} identifiers checked, {len(bad)} problems")
    print("\n".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
