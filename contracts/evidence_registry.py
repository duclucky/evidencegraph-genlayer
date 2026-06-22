"""Deterministic in-memory registry for EvidenceGraph evidence packages."""

from copy import deepcopy
from datetime import datetime, timezone
import json


class EvidenceRegistry:
    """Register immutable evidence inputs and attach a later review record."""

    def __init__(self, clock=None):
        self._packages = {}
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def register_evidence_package(
        self,
        claim_title,
        claim_description,
        evidence_package_json,
        evidence_hash,
        source_url="",
        submitter="local-user",
    ):
        title = str(claim_title or "").strip()
        description = str(claim_description or "").strip()
        package_json = str(evidence_package_json or "").strip()
        package_hash = str(evidence_hash or "").strip()
        if not title:
            raise ValueError("claim_title is required")
        if not package_json:
            raise ValueError("evidence_package_json is required")
        try:
            parsed_package = json.loads(package_json)
        except json.JSONDecodeError as error:
            raise ValueError("evidence_package_json must be valid JSON") from error
        if not isinstance(parsed_package, dict):
            raise ValueError("evidence_package_json must contain a JSON object")
        if not package_hash:
            raise ValueError("evidence_hash is required")

        package_id = f"package_{len(self._packages) + 1}"
        self._packages[package_id] = {
            "package_id": package_id,
            "submitter": str(submitter or "local-user").strip() or "local-user",
            "claim_title": title,
            "claim_description": description,
            "evidence_package_json": package_json,
            "evidence_hash": package_hash,
            "source_url": str(source_url or "").strip(),
            "status": "registered",
            "created_at": self._timestamp(),
            "reviewed_at": "",
            "verdict": "",
            "review_note": "",
        }
        return package_id

    def get_evidence_package(self, package_id):
        return deepcopy(self._require_package(package_id))

    def get_package_count(self):
        return len(self._packages)

    def mark_package_reviewed(self, package_id, verdict, note):
        package = self._require_package(package_id)
        normalized_verdict = str(verdict or "").strip()
        if not normalized_verdict:
            raise ValueError("verdict is required")
        package["status"] = "reviewed"
        package["reviewed_at"] = self._timestamp()
        package["verdict"] = normalized_verdict
        package["review_note"] = str(note or "").strip()
        return self.get_review(package_id)

    def get_review(self, package_id):
        package = self._require_package(package_id)
        return {
            "package_id": package["package_id"],
            "status": package["status"],
            "reviewed_at": package["reviewed_at"],
            "verdict": package["verdict"],
            "review_note": package["review_note"],
        }

    def _require_package(self, package_id):
        if package_id not in self._packages:
            raise KeyError(f"Unknown evidence package: {package_id}")
        return self._packages[package_id]

    def _timestamp(self):
        value = self._clock()
        if not isinstance(value, datetime):
            raise TypeError("clock must return a datetime")
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
