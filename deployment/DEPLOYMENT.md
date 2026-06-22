# EvidenceGraph On-chain Registry Deployment

## Current status

EvidenceGraph v1.1 includes a deterministic local registry at `contracts/evidence_registry.py` and a GenLayer-style deployment draft at `contracts/evidence_registry_genlayer.py`. The registry stores structured evidence JSON, its content hash, source metadata, registration status, and a later review record.

The module is deployment-ready documentation and reference logic, but it has **not** been deployed. No network, contract address, or transaction hash should be claimed until they are verified from an actual deployment.

## Contract draft

`contracts/evidence_registry_genlayer.py` maps the local API into intended public write/view sections and documents persistent storage. SDK imports and decorators remain comments because the project does not pin or invent an unverified GenLayer API.

Before deployment, adapt the draft against the current official GenLayer SDK and runtime documentation:

1. Replace the in-memory registry with documented persistent storage.
2. Apply the supported public write/view decorators.
3. Derive the submitter from documented transaction context.
4. Define who may call `mark_package_reviewed`.
5. Define consensus-safe timestamp behavior.
6. Run contract-runtime tests against the selected environment.

## Manual deployment later

### GenLayer Studio

1. Open GenLayer Studio for the intended network.
2. Create/import an Intelligent Contract using the adapted registry draft.
3. Confirm SDK imports, storage declarations, decorators, and constructor behavior against the Studio runtime.
4. Deploy from the authorized wallet/account.
5. Copy the verified network, contract address, and deployment transaction hash.
6. Call `register_evidence_package` with an EvidenceGraph JSON package and its content hash.
7. Copy the returned package ID and registration transaction hash.

### GenLayer CLI

Use the official CLI documentation for the installed version. This repository intentionally does not provide guessed CLI commands. Select the network, deploy the verified contract source, then invoke `register_evidence_package` and record the same fields listed below.

## Deployment evidence to record

Copy `deployment/deployment_info.example.json` to a deployment-specific record and fill in:

- `network`
- `contract_address`
- `deploy_transaction_hash`
- `example_register_transaction_hash`
- `registered_package_id`
- `deployed_at`

Keep the blank example file unchanged for future environments. Verify every address/hash in the relevant network explorer or GenLayer tooling before publishing it.

## Update the Portal submission

After deployment, replace these placeholders in `SUBMISSION.md`:

- `[NETWORK]`
- `[CONTRACT_ADDRESS]`
- `[DEPLOY_TRANSACTION_HASH]`
- `[REGISTER_EVIDENCE_TRANSACTION_HASH]`
- `[REGISTERED_PACKAGE_ID]`

Do not replace placeholders with local mock values. Keep the Vercel, GitHub, and demo-video links unchanged unless those public artifacts move.
