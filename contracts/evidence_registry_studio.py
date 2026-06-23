# { "Depends": "py-genlayer:latest" }
"""EvidenceGraph On-chain Registry — GenLayer Studio deployable contract.

Self-contained Intelligent Contract for studio.genlayer.com. It has no local
project imports and no external libraries: paste this entire file into the
Studio editor and deploy.

The contract stores evidence packages and their later review records as compact
JSON strings in on-chain persistent storage. It is fully deterministic and makes
no LLM calls and no web calls.
"""

from genlayer import *


def _esc(value: str) -> str:
    """Escape a string so it is safe to embed inside a JSON string literal."""
    out = ""
    for ch in value:
        if ch == '"':
            out += '\\"'
        elif ch == "\\":
            out += "\\\\"
        elif ch == "\n":
            out += "\\n"
        elif ch == "\r":
            out += "\\r"
        elif ch == "\t":
            out += "\\t"
        else:
            out += ch
    return out


def _field(name: str, value: str, last: bool = False) -> str:
    """Render a single "name":"value" JSON pair, with a trailing comma unless last."""
    pair = '"' + _esc(name) + '":"' + _esc(value) + '"'
    return pair if last else pair + ","


class Contract(gl.Contract):
    # On-chain persistent storage.
    package_count: u256
    packages: TreeMap[str, str]
    reviews: TreeMap[str, str]

    def __init__(self):
        self.package_count = u256(0)

    @gl.public.write
    def register_evidence_package(
        self,
        claim_title: str,
        claim_description: str,
        evidence_package_json: str,
        evidence_hash: str,
        source_url: str,
    ) -> str:
        # Increment the counter and derive a stable, human-readable package id.
        self.package_count += u256(1)
        package_id = "package_" + str(self.package_count)

        record = (
            "{"
            + _field("package_id", package_id)
            + _field("claim_title", claim_title)
            + _field("claim_description", claim_description)
            + _field("evidence_package_json", evidence_package_json)
            + _field("evidence_hash", evidence_hash)
            + _field("source_url", source_url)
            + _field("status", "registered", last=True)
            + "}"
        )

        self.packages[package_id] = record
        return package_id

    @gl.public.view
    def get_evidence_package(self, package_id: str) -> str:
        if package_id in self.packages:
            return self.packages[package_id]
        return ""

    @gl.public.view
    def get_package_count(self) -> u256:
        return self.package_count

    @gl.public.write
    def mark_package_reviewed(self, package_id: str, verdict: str, note: str) -> bool:
        review = (
            "{"
            + _field("package_id", package_id)
            + _field("verdict", verdict)
            + _field("note", note)
            + _field("status", "reviewed", last=True)
            + "}"
        )

        self.reviews[package_id] = review
        return True

    @gl.public.view
    def get_review(self, package_id: str) -> str:
        if package_id in self.reviews:
            return self.reviews[package_id]
        return ""
