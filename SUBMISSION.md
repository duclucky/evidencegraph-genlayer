# EvidenceGraph — GenLayer Portal Submission

## Builder → Projects summary

- Project name: **EvidenceGraph**
- Category: **Developer tooling / Intelligent Contract infrastructure**
- One-line pitch: **Prepare, score, and register structured evidence before an Intelligent Contract reasons over it.**
- Primary users: GenLayer builders preparing milestone, grant, SLA, dispute, and public-event evidence

## Project

**EvidenceGraph v1.1** is an AI Evidence Pack Builder with an On-chain Evidence Registry for GenLayer Intelligent Contracts. It transforms raw claims and scattered source links into structured packages with explainable quality scores, missing-proof detection, manipulation risk, GenLayer-ready JSON, and a contract registration path.

## Problem and solution

Intelligent Contracts often need to judge natural-language claims using unstructured public evidence. EvidenceGraph improves those inputs before judgment begins. Builders can assemble repositories, releases, demos, documentation, test results, screenshots, transactions, articles, and logs; then receive a deterministic readiness review and a portable JSON package.

EvidenceGraph does not decide the final dispute outcome. It is an evidence preparation layer that helps downstream Intelligent Contracts reason over clearer, more complete, and harder-to-manipulate inputs.

## Links and deployment details

- GitHub repo URL: [https://github.com/duclucky/evidencegraph-genlayer](https://github.com/duclucky/evidencegraph-genlayer)
- Vercel frontend URL: [https://evidencegraph-genlayer.vercel.app](https://evidencegraph-genlayer.vercel.app)
- Demo video artifact: [media/evidencegraph_demo.mp4](media/evidencegraph_demo.mp4)
- Hosted demo video URL: [https://github.com/duclucky/evidencegraph-genlayer/blob/main/media/evidencegraph_demo.mp4](https://github.com/duclucky/evidencegraph-genlayer/blob/main/media/evidencegraph_demo.mp4)
- Network: `[NETWORK]`
- Contract address: `[CONTRACT_ADDRESS]`
- Deploy transaction hash: `[DEPLOY_TRANSACTION_HASH]`
- Register evidence transaction hash: `[REGISTER_EVIDENCE_TRANSACTION_HASH]`
- Registered package ID: `[REGISTERED_PACKAGE_ID]`

## Key features

- Five-part, 100-point evidence quality rubric
- Missing-evidence and manipulation-risk detection
- GenLayer use-case alignment and readiness score
- Weak and strong example packs for instant comparison
- Structured `evidencegraph.v1` JSON output
- Static, webapp-first frontend and plain Python reference logic
- GenLayer-style contract draft with explicit LLM and web-verification extension points
- On-chain Evidence Registry reference implementation with preserved evidence hashes
- Copy-ready network, contract, deployment transaction, and registration transaction evidence
- Registry deployment draft and manual deployment record template

## What makes it different

EvidenceGraph is not an escrow, bounty platform, prediction market, or court/arbitration clone. It does not hold funds or choose a winner. It sits one layer earlier: it evaluates whether the evidence supplied to an Intelligent Contract is complete, relevant, independently sourced, resistant to manipulation, and structured enough for contract consumption.

## Technical implementation

The webapp is dependency-free HTML, CSS, and JavaScript hosted directly from the repository root. A plain Python scoring class provides the intended submit, review, retrieve, count, and export API with a deterministic 100-point rubric. A separate `EvidenceRegistry` class registers the exported `evidencegraph.v1` JSON and content hash, then stores later review metadata without changing the registered proof. Both GenLayer contract files are explicitly marked as deployment drafts until a verified SDK version and network deployment are available.

## Reviewer demo path

1. Open the frontend and load **Weak self-claim**.
2. Review it to see missing independent/timestamped evidence and high manipulation risk.
3. Load **Strong milestone pack** and review the repo, release, docs, demo, and tests.
4. Compare the score and verdict, then expand `contract_input` in the JSON preview.
5. Open **On-chain Registry** to preview the package and copy the deployment evidence block.

## GenLayer fit

Milestones, grants, agent SLAs, disputes, and public event claims frequently require natural-language judgment across multiple web sources. EvidenceGraph normalizes and scores those sources so a GenLayer Intelligent Contract receives a higher-quality reasoning context. Future integration can use documented GenLayer LLM and web primitives for semantic relevance and live source verification.

## Current status

EvidenceGraph v1.1 includes the browser MVP, deterministic scoring engine, local registry, registry tests, deployment evidence UI, and two GenLayer-style contract drafts. It is not yet deployed. Replace the on-chain placeholders only with verified network, contract, deployment transaction, registration transaction, and package ID details after a tested deployment.
