# EvidenceGraph

**AI Evidence Pack Builder for GenLayer Intelligent Contracts.**

**Live demo:** [https://evidencegraph-genlayer.vercel.app](https://evidencegraph-genlayer.vercel.app)

EvidenceGraph turns raw claims, URLs, repository links, demos, screenshots, documentation, logs, and transaction references into structured evidence packages with quality scores, missing-proof detection, manipulation risk, and GenLayer-ready JSON.

## Problem

Intelligent Contracts can reason over natural language and unstructured web evidence, but the inputs builders provide are often scattered, vague, self-authored, or difficult to verify. Poor evidence preparation weakens the quality of downstream reasoning.

For an Intelligent Contract, evidence quality is input quality: missing context, unverifiable sources, or easy-to-manipulate proof can produce a fragile judgment even when the reasoning layer is capable. EvidenceGraph makes those weaknesses visible before contract execution and preserves them as explicit quality signals rather than hiding them inside a final answer.

## Solution

EvidenceGraph is an evidence preparation and quality-scoring layer. It gives builders immediate, deterministic feedback before an evidence pack reaches an Intelligent Contract. It is not an escrow, bounty, prediction market, court, or final dispute resolver; it improves the inputs to those systems.

## Why GenLayer

Many real claims cannot be resolved from a single numeric oracle. Milestone completion, grant progress, agent SLA performance, and public-event evidence require judgment across natural language and web sources. GenLayer Intelligent Contracts are a natural downstream consumer for EvidenceGraph's structured packages. A future contract version can add LLM-based semantic review and web verification while retaining the deterministic rubric as an explainable baseline.

## Features

- Browser-first claim and evidence builder with no server or wallet required
- Ten evidence types, including repositories, releases, demos, tests, transactions, and logs
- Scores for completeness, source quality, relevance, manipulation resistance, and GenLayer readiness
- Source strength, manipulation risk, readiness, verdict, missing evidence, and recommendations
- Copyable `evidencegraph.v1` JSON package
- Dedicated `contract_input` payload with normalized claim, evidence, use case, and quality gate
- Weak and strong sample packs for a fast demo
- Plain Python reference engine and GenLayer-style deployment draft

## Demo flow

1. Open the app and select **Weak self-claim**.
2. Review it to expose missing independent, timestamped proof and high manipulation risk.
3. Select **Strong milestone pack**.
4. Review the public repo, release, docs, demo, and tests.
5. Expand the JSON output to show the contract-consumable package.

See [DEMO.md](DEMO.md) for a two-minute script.

Automated no-audio demo video: [media/evidencegraph_demo.mp4](media/evidencegraph_demo.mp4) — 105 seconds, 1920×1080, with seven captioned scenes covering the problem, solution, weak and strong evidence packs, GenLayer fit, and closing position.

## Architecture

```text
index.html + styles.css
        │
        └── app.js ── deterministic browser scoring ── JSON preview

contracts/evidence_graph.py
        ├── in-memory evidence pack storage
        ├── deterministic scoring and recommendations
        └── JSON export

contracts/evidence_graph_genlayer.py
        └── deployment draft with explicit SDK integration placeholders
```

The browser and Python engine implement the same rubric independently. The static app is the MVP experience; the Python class defines the intended contract-facing API. Exported packages contain the full human-readable review plus a compact `contract_input` object designed for downstream Intelligent Contract consumption.

## Scoring rubric

| Category | Max | Main signals |
|---|---:|---|
| Completeness | 30 | Clear claim, two or more items, independent source, use-case evidence |
| Source quality | 25 | Public repositories, releases, docs, demos, tests, transactions |
| Relevance | 20 | Evidence types aligned with the selected use case |
| Manipulation resistance | 15 | Public links, timestamps, independent domains, hard-to-fake proof |
| GenLayer readiness | 10 | Structured output, judgment use case, descriptive claim, multiple items |

The total is the exact sum of all five sub-scores. The MVP is heuristic and deterministic; it does not claim that a source is true merely because a URL is present.

## Run the frontend locally

No installation or build is required. Double-click `index.html`, or right-click it and choose **Open with** followed by a modern browser. All scoring runs locally in the page.

## Run the tests

From the repository root:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Run this command in a local PowerShell session. The test suite uses Python's standard-library `unittest` only and requires no package installation. A Codex sandbox may block `python.exe` before it starts; that sandbox restriction is not evidence of a project or test failure. Record the authoritative result from local PowerShell in `TESTING.md`.

Latest verified local result (2026-06-23): **9 tests passed, 0 failures (`OK`)** in 0.008 seconds. See `TESTING.md` for the recorded output summary.

## Deploy to Vercel

Import the repository into Vercel and use:

- Framework Preset: **Other**
- Root Directory: repository root
- Build Command: leave empty
- Output Directory: leave empty or set to `.`
- Install Command: leave empty

No `vercel.json` is required because `index.html` is at the repository root and the app has no client-side routes.

If Vercel returns a 404, confirm that **Root Directory** points to the directory that directly contains `index.html`; do not select `contracts`, `media`, or a nonexistent `frontend` folder. Also remove any inherited build or output-directory override. The deployment must publish the repository root as static files.

## GenLayer integration notes

`contracts/evidence_graph_genlayer.py` is deliberately a deployment draft, not a verified deployed contract. It preserves the public method surface, identifies persistent storage, and marks intended public write/view sections. SDK imports and decorators are comments because this repository does not pin or assume an unsupported GenLayer API.

Before deployment, select a verified SDK version, replace in-memory dictionaries with persistent storage, implement LLM and web access through documented primitives, define consensus-safe outputs, and add contract-runtime tests.

## Limitations

- URLs are scored by their shape and evidence type; the static MVP does not fetch or verify them.
- Semantic relevance is approximated from use-case and evidence-type matching.
- Storage is in memory and resets when the Python process ends.
- Browser and Python implementations must be kept aligned when the rubric changes.
- The GenLayer draft has not been deployed or verified against a live SDK/runtime.

## Future improvements

- Live source availability and metadata verification
- LLM-based claim-to-evidence relevance analysis
- Duplicate, conflicting, and suspicious-source detection
- Signed evidence manifests and content hashes
- Import/export history and collaborative packs
- Verified GenLayer contract deployment with consensus-safe web review
