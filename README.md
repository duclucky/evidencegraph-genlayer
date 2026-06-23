# EvidenceGraph v1.1

**Prepare, score, and register structured evidence packages for GenLayer Intelligent Contracts.**

**Live demo:** [https://evidencegraph-genlayer.vercel.app](https://evidencegraph-genlayer.vercel.app)

EvidenceGraph turns raw claims, URLs, repository links, demos, screenshots, documentation, logs, and transaction references into structured evidence packages with quality scores, missing-proof detection, manipulation risk, GenLayer-ready JSON, and an on-chain registration path.

## Problem

Intelligent Contracts can reason over natural language and unstructured web evidence, but the inputs builders provide are often scattered, vague, self-authored, or difficult to verify. Poor evidence preparation weakens the quality of downstream reasoning.

For an Intelligent Contract, evidence quality is input quality: missing context, unverifiable sources, or easy-to-manipulate proof can produce a fragile judgment even when the reasoning layer is capable. EvidenceGraph makes those weaknesses visible before contract execution and preserves them as explicit quality signals rather than hiding them inside a final answer.

## Solution

EvidenceGraph is an evidence preparation, quality-scoring, and registration layer. It gives builders immediate, deterministic feedback before an evidence pack reaches an Intelligent Contract, then provides a registry module for anchoring the package JSON and evidence hash. It is not an escrow, bounty, prediction market, court, or final dispute resolver; it improves and records the inputs to those systems.

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
- On-chain Evidence Registry reference logic with immutable package hash preservation
- Deployment evidence UI for network, contract address, and transaction hashes
- GenLayer-style registry contract draft and manual deployment checklist

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

The browser and Python engine implement the same rubric independently. The static app is the MVP experience; the Python class defines the intended contract-facing API. Exported packages contain the full human-readable review plus a compact `contract_input` object designed for downstream Intelligent Contract consumption. The separate registry module owns registration and review state so the scoring rubric remains unchanged.

The v1.1 architecture also includes `contracts/evidence_registry.py` for deterministic local registration, `contracts/evidence_registry_genlayer.py` for the GenLayer-style deployment draft, and `deployment/` for deployment instructions and evidence metadata.

## On-chain Evidence Registry

EvidenceGraph v1.1 adds the **EvidenceGraph On-chain Registry** (internally, the ProofStamp module). The local registry stores an EvidenceGraph JSON package together with its content hash, source URL, submitter, timestamp, status, and later review metadata. The registered evidence JSON and hash are preserved when a review is attached.

This upgrade prevents the project from being only a static scoring page: the webapp prepares a deterministic registry payload and copy-ready deployment evidence, while the registry API defines how an Intelligent Contract can persist package identity and review state. The current browser remains connection-free by design; it does not pretend that a local preview is an on-chain transaction.

After a real deployment, the module produces verifiable Portal evidence: GenLayer network, registry contract address, contract deployment transaction hash, example evidence-registration transaction hash, review transaction hash, and registered package ID. See the **Live GenLayer Deployment** section below, [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md), and [deployment/deployment_info.json](deployment/deployment_info.json).

## Live GenLayer Deployment

The Studio-ready registry contract ([contracts/evidence_registry_studio.py](contracts/evidence_registry_studio.py)) is **deployed and verified on the GenLayer Bradbury Testnet**.

| Field | Value |
|---|---|
| Network | GenLayer Bradbury Testnet |
| Contract address | `0xd09032a85dB930dCdE10994579a80D0d70fe3E15` |
| Deploy transaction hash | `0x5d18235a344652f8e86d5c9136526215135413c4277f6ad6cfa894686c2218ef` |
| Register evidence transaction hash | `0x4895a86adb04e6b2041319341e2caf429da0dd303167daf934ebbd64f8a4ee6f` |
| Review transaction hash | `0xc8113b2d9a487a9ba682f35a96bfa752fec5bc84fa1c8ed3b89994768f291d6d` |
| Registered package ID | `package_1` |
| Deployed at | 2026-06-23 |

The deploy transaction created the registry, the register-evidence transaction stored an `evidencegraph.v1` package with its content hash, and the review transaction attached a review record without changing the registered evidence. Full machine-readable record: [deployment/deployment_info.json](deployment/deployment_info.json).

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

Verified v1.0 baseline (2026-06-23): **9 tests passed, 0 failures (`OK`)** in 0.008 seconds. EvidenceGraph v1.1 adds the registry suite, which is awaiting a fresh local run. See `TESTING.md` for the recorded status.

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

`contracts/evidence_graph_genlayer.py` and `contracts/evidence_registry_genlayer.py` are deliberately deployment drafts, not verified deployed contracts. They preserve the intended public method surfaces, identify persistent storage, and mark intended public write/view sections. SDK imports and decorators are comments because this repository does not pin or assume an unsupported GenLayer API.

Before deployment, select a verified SDK version, replace in-memory dictionaries with persistent storage, implement LLM and web access through documented primitives, define consensus-safe outputs, and add contract-runtime tests.

## Limitations

- URLs are scored by their shape and evidence type; the static MVP does not fetch or verify them.
- Semantic relevance is approximated from use-case and evidence-type matching.
- Local scoring and registry storage are in memory and reset when the Python process ends.
- Browser and Python implementations must be kept aligned when the rubric changes.
- The two `*_genlayer.py` files remain non-deployable drafts; the deployed contract is `contracts/evidence_registry_studio.py` on the GenLayer Bradbury Testnet.

## Future improvements

- Live source availability and metadata verification
- LLM-based claim-to-evidence relevance analysis
- Duplicate, conflicting, and suspicious-source detection
- Signed evidence manifests and content hashes
- Import/export history and collaborative packs
- Verified GenLayer contract deployment with consensus-safe web review
