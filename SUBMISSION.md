# EvidenceGraph — GenLayer Portal Submission

## Builder → Projects summary

- Project name: **EvidenceGraph**
- Category: **Developer tooling / Intelligent Contract infrastructure**
- One-line pitch: **Prepare, score, and structure web evidence before an Intelligent Contract reasons over it.**
- Primary users: GenLayer builders preparing milestone, grant, SLA, dispute, and public-event evidence

## Project

**EvidenceGraph** is an AI Evidence Pack Builder for GenLayer Intelligent Contracts. It transforms raw claims and scattered source links into structured packages with explainable quality scores, missing-proof detection, manipulation risk, and GenLayer-ready JSON.

## Problem and solution

Intelligent Contracts often need to judge natural-language claims using unstructured public evidence. EvidenceGraph improves those inputs before judgment begins. Builders can assemble repositories, releases, demos, documentation, test results, screenshots, transactions, articles, and logs; then receive a deterministic readiness review and a portable JSON package.

EvidenceGraph does not decide the final dispute outcome. It is an evidence preparation layer that helps downstream Intelligent Contracts reason over clearer, more complete, and harder-to-manipulate inputs.

## Links and deployment details

- GitHub repo URL: `[GITHUB_REPO_URL]`
- Vercel frontend URL: [https://evidencegraph-genlayer.vercel.app](https://evidencegraph-genlayer.vercel.app)
- Demo video artifact: [media/evidencegraph_demo.mp4](media/evidencegraph_demo.mp4)
- Hosted demo video URL: `[DEMO_VIDEO_URL]`
- Network: `[NETWORK]`
- Contract address: `[CONTRACT_ADDRESS]`
- Transaction hash: `[TRANSACTION_HASH]`

## Key features

- Five-part, 100-point evidence quality rubric
- Missing-evidence and manipulation-risk detection
- GenLayer use-case alignment and readiness score
- Weak and strong example packs for instant comparison
- Structured `evidencegraph.v1` JSON output
- Static, webapp-first frontend and plain Python reference logic
- GenLayer-style contract draft with explicit LLM and web-verification extension points

## What makes it different

EvidenceGraph is not an escrow, bounty platform, prediction market, or court/arbitration clone. It does not hold funds or choose a winner. It sits one layer earlier: it evaluates whether the evidence supplied to an Intelligent Contract is complete, relevant, independently sourced, resistant to manipulation, and structured enough for contract consumption.

## Technical implementation

The webapp is dependency-free HTML, CSS, and JavaScript hosted directly from the repository root. A plain Python reference class provides the intended submit, review, retrieve, count, and export API with in-memory storage and a deterministic 100-point rubric. The exported `evidencegraph.v1` object includes a compact `contract_input` section for downstream use. The GenLayer contract file is explicitly marked as a deployment draft until a verified SDK version and network deployment are available.

## Reviewer demo path

1. Open the frontend and load **Weak self-claim**.
2. Review it to see missing independent/timestamped evidence and high manipulation risk.
3. Load **Strong milestone pack** and review the repo, release, docs, demo, and tests.
4. Compare the score and verdict, then expand `contract_input` in the JSON preview.

## GenLayer fit

Milestones, grants, agent SLAs, disputes, and public event claims frequently require natural-language judgment across multiple web sources. EvidenceGraph normalizes and scores those sources so a GenLayer Intelligent Contract receives a higher-quality reasoning context. Future integration can use documented GenLayer LLM and web primitives for semantic relevance and live source verification.

## Current status

The browser MVP and local deterministic scoring engine are prepared. `contracts/evidence_graph_genlayer.py` is a deployment draft only; replace these placeholders with verified network, contract, and transaction details after a tested deployment.
