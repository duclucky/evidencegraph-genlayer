# Testing EvidenceGraph

## Scope

The test suite covers EvidenceGraph scoring plus the v1.1 On-chain Evidence Registry. Registry coverage includes package registration, retrieval, count increments, review updates, stored review data, and evidence-hash preservation. It uses only Python's standard-library `unittest`.

## Authoritative local command

Run from the repository root in local PowerShell:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

## Expected behavior

The command should discover both `tests/test_evidence_graph.py` and `tests/test_evidence_registry.py`, then print one result per test. A successful run ends with `OK`. No npm install, Python package install, server, GenLayer CLI, or network access is needed.

## Codex sandbox note — 2026-06-23

The Codex sandbox blocked `python.exe` before the interpreter or test discovery started. This is a Codex sandbox limitation, not a project failure, Python installation failure, or test result. No environment changes or workaround installations are required. Local PowerShell output from the command above is the authoritative test result.

## Local test result

Status: **v1.0 baseline passed; v1.1 registry suite awaiting local verification**

- Execution date: 2026-06-23
- Environment: Local PowerShell
- Command: `python -m unittest discover -s tests -p "test_*.py" -v`
- Tests run: 9
- Passed: 9
- Failed: 0
- Errors: 0
- Duration: 0.008 seconds
- Final result: `OK`

The verified 9-test result above predates the v1.1 registry module. It covers evidence package export, pack counting, retrieval, strong and weak reviews, submission, score arithmetic, unknown-pack handling, and verdict/risk changes. Run the authoritative command again locally to verify the combined scoring and registry suite; replace this note with the new total and output summary afterward.

## Registry test coverage awaiting verification

- Register an evidence package
- Retrieve the complete stored package
- Increment the package count
- Mark a package reviewed
- Persist verdict, review timestamp, and note
- Preserve the exact evidence hash

## Manual browser check

1. Open `index.html` directly in a modern browser.
2. Load **Weak self-claim**, review it, and confirm a weak/high-risk result with missing evidence.
3. Load **Strong milestone pack**, review it, and confirm an evidence-ready, low-risk result.
4. Expand the JSON preview and confirm it includes `pack` and `review`.
5. Resize the browser to a narrow mobile width and confirm the form and result stack vertically.

## Important MVP caveat

The browser does not contact the Python class. Both implement the same deterministic rubric so the app remains a zero-server static site. Changes to scoring should update both implementations and their tests together.
