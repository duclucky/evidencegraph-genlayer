import json
import unittest
from datetime import datetime, timezone

from contracts.evidence_registry import EvidenceRegistry


class EvidenceRegistryTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 6, 23, 12, 0, tzinfo=timezone.utc)
        self.registry = EvidenceRegistry(clock=lambda: self.now)
        self.package_json = json.dumps({
            "schema_version": "evidencegraph.v1",
            "pack": {"claim_title": "Milestone shipped"},
            "review": {"evidence_score": 92, "verdict": "evidence_ready"},
        })

    def _register(self, evidence_hash="sha256:abc123"):
        return self.registry.register_evidence_package(
            "Milestone shipped",
            "The release contains the agreed milestone and passing tests.",
            self.package_json,
            evidence_hash,
            "https://evidencegraph-genlayer.vercel.app",
            "builder-0x123",
        )

    def test_register_evidence_package(self):
        package_id = self._register()
        package = self.registry.get_evidence_package(package_id)

        self.assertEqual("package_1", package_id)
        self.assertEqual("registered", package["status"])
        self.assertEqual("builder-0x123", package["submitter"])
        self.assertEqual(self.now.isoformat(), package["created_at"])

    def test_retrieve_evidence_package(self):
        package_id = self._register()
        package = self.registry.get_evidence_package(package_id)

        self.assertEqual("Milestone shipped", package["claim_title"])
        self.assertEqual(self.package_json, package["evidence_package_json"])
        self.assertEqual("https://evidencegraph-genlayer.vercel.app", package["source_url"])

    def test_package_count_increments(self):
        self.assertEqual(0, self.registry.get_package_count())
        self._register()
        self._register("sha256:def456")
        self.assertEqual(2, self.registry.get_package_count())

    def test_mark_package_reviewed(self):
        package_id = self._register()
        review = self.registry.mark_package_reviewed(
            package_id, "evidence_ready", "Verified against the release and tests."
        )

        self.assertEqual("reviewed", self.registry.get_evidence_package(package_id)["status"])
        self.assertEqual("evidence_ready", review["verdict"])
        self.assertEqual(self.now.isoformat(), review["reviewed_at"])

    def test_review_data_is_stored(self):
        package_id = self._register()
        self.registry.mark_package_reviewed(package_id, "needs_more_sources", "Add an independent source.")

        review = self.registry.get_review(package_id)
        self.assertEqual("needs_more_sources", review["verdict"])
        self.assertEqual("Add an independent source.", review["review_note"])
        self.assertEqual(package_id, review["package_id"])

    def test_evidence_hash_is_preserved(self):
        evidence_hash = "sha256:9c56cc51b374c3ba189210d5b6d4bf57790d351c96c47c02190ecf1e430635ab"
        package_id = self._register(evidence_hash)
        self.assertEqual(evidence_hash, self.registry.get_evidence_package(package_id)["evidence_hash"])


if __name__ == "__main__":
    unittest.main()
