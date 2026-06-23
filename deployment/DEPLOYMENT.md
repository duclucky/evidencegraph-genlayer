# EvidenceGraph On-chain Registry Deployment

## Current status

EvidenceGraph v1.1 includes a deterministic local registry at `contracts/evidence_registry.py`, a Studio-ready contract at `contracts/evidence_registry_studio.py`, and a GenLayer-style deployment draft at `contracts/evidence_registry_genlayer.py`. The registry stores structured evidence JSON, its content hash, source metadata, registration status, and a later review record.

The Studio-ready contract has been **deployed and verified** on the GenLayer Bradbury Testnet. See the live deployment details below.

## Live deployment

| Field | Value |
|---|---|
| Network | GenLayer Bradbury Testnet |
| Contract address | `0xd09032a85dB930dCdE10994579a80D0d70fe3E15` |
| Deploy transaction hash | `0x5d18235a344652f8e86d5c9136526215135413c4277f6ad6cfa894686c2218ef` |
| Register evidence transaction hash | `0x4895a86adb04e6b2041319341e2caf429da0dd303167daf934ebbd64f8a4ee6f` |
| Review transaction hash | `0xc8113b2d9a487a9ba682f35a96bfa752fec5bc84fa1c8ed3b89994768f291d6d` |
| Registered package ID | `package_1` |
| Deployed at | 2026-06-23 |

The verified deployment record is in [deployment/deployment_info.json](deployment_info.json). Verify every address and hash in the GenLayer Bradbury explorer before republishing it elsewhere.

## Contract draft

`contracts/evidence_registry_genlayer.py` maps the local API into intended public write/view sections and documents persistent storage. SDK imports and decorators remain comments because the project does not pin or invent an unverified GenLayer API.

Before deployment, adapt the draft against the current official GenLayer SDK and runtime documentation:

1. Replace the in-memory registry with documented persistent storage.
2. Apply the supported public write/view decorators.
3. Derive the submitter from documented transaction context.
4. Define who may call `mark_package_reviewed`.
5. Define consensus-safe timestamp behavior.
6. Run contract-runtime tests against the selected environment.

## Studio-ready contract

`contracts/evidence_registry_studio.py` is a fully self-contained, paste-ready GenLayer Studio contract. Unlike the draft above, it has **no local imports and no external libraries** (only `from genlayer import *`): it uses typed persistent storage (`u256` counter, `TreeMap[str, str]` for packages and reviews), `@gl.public.write`/`@gl.public.view` decorators, and a no-argument constructor. It is deterministic and makes no LLM or web calls. Paste the whole file into studio.genlayer.com to deploy.

## Manual deployment later

### GenLayer Studio

1. Open GenLayer Studio for the intended network.
2. Create a new Intelligent Contract and paste `contracts/evidence_registry_studio.py` (or import the adapted registry draft).
3. Confirm SDK imports, storage declarations, decorators, and constructor behavior against the Studio runtime.
4. Deploy from the authorized wallet/account.
5. Copy the verified network, contract address, and deployment transaction hash.
6. Call `register_evidence_package` with an EvidenceGraph JSON package and its content hash.
7. Copy the returned package ID and registration transaction hash.

### GenLayer CLI

Use the official CLI documentation for the installed version. This repository intentionally does not provide guessed CLI commands. Select the network, deploy the verified contract source, then invoke `register_evidence_package` and record the same fields listed below.

## Deployment evidence record

The verified Bradbury Testnet deployment is recorded in `deployment/deployment_info.json` with:

- `network`
- `contract_address`
- `deploy_transaction_hash`
- `example_register_transaction_hash`
- `review_transaction_hash`
- `registered_package_id`
- `deployed_at`

`deployment/deployment_info.example.json` remains a blank template for future environments. Verify every address/hash in the relevant network explorer or GenLayer tooling before republishing it.

## Portal submission

`SUBMISSION.md` and `README.md` carry the live network, contract address, deploy/register/review transaction hashes, and registered package ID. Keep the Vercel, GitHub, and demo-video links unchanged unless those public artifacts move.
