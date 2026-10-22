# Mapping without Python

Use when `scripts/hotspots.py` cannot run (no `python`/`python3`/`py`, common in sandboxed
agents on Windows where those are app aliases). Replace `src` with the perimeter.

If git refuses the repo ("dubious ownership"), add `-c safe.directory=*` after `git`.

## bash / zsh

```bash
# churn: most changed files
git -c safe.directory=* log -n 300 --name-only --format= -- src | sort | uniq -c | sort -rn | head -20
# size
find src -type f \( -name '*.py' -o -name '*.js' -o -name '*.ts' -o -name '*.java' -o -name '*.cs' \) \
  -not -path '*/node_modules/*' -not -path '*/test*' | xargs wc -l | sort -rn | head -20
# repeated type-code comparisons (attribute == "literal")
grep -rEoh "\w+\s*[!=]==?\s*['\"][A-Za-z0-9_-]+['\"]" src | sed -E 's/\s*[!=]=.*//' | sort | uniq -c | sort -rn | head -20
```

## PowerShell

```powershell
# churn
git -c safe.directory=* log -n 300 --name-only --format= -- src | Where-Object { $_ } | Group-Object | Sort-Object Count -Descending | Select-Object -First 20 Count, Name
# size
Get-ChildItem src -Recurse -File -Include *.py,*.js,*.ts,*.java,*.cs | Where-Object { $_.FullName -notmatch 'node_modules|[\\/]tests?[\\/]' } | ForEach-Object { [pscustomobject]@{ Lines = (Get-Content $_.FullName | Measure-Object -Line).Lines; File = $_.FullName } } | Sort-Object Lines -Descending | Select-Object -First 20
# repeated type-code comparisons
Get-ChildItem src -Recurse -File -Include *.py,*.js,*.ts,*.java,*.cs,*.go,*.rb,*.php | Select-String -Pattern '(\w+)\s*[!=]==?\s*[''"][\w-]+[''"]' -AllMatches | ForEach-Object { $_.Matches.ForEach({ $_.Groups[1].Value }) } | Group-Object | Sort-Object Count -Descending | Select-Object -First 20 Count, Name
```

Read the type-code list as leads: an attribute compared against several literals in several
places is a Switch Statements candidate; `typeof x === "undefined"` checks are not.
