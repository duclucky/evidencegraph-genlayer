import json
import unittest

from contracts.evidence_graph import EvidenceGraph


class EvidenceGraphTests(unittest.TestCase):
    def setUp(self):
        self.graph = EvidenceGraph()

    def _strong_pack(self):
        return self.graph.submit_evidence_pack(
            "Milestone shipped with reproducible tests",
            "The public release implements the milestone and its tests pass.",
            [
                {"url": "https://github.com/example/project", "type": "github_repo", "description": "Public source repository"},
                {"url": "https://github.com/example/project/releases/tag/v1.0.0", "type": "commit_release", "description": "Timestamped release"},
                {"url": "https://docs.example.org/milestone", "type": "documentation", "description": "Independent public documentation"},
                {"url": "https://youtu.be/example", "type": "demo_video", "description": "Working product demo"},
                {"url": "https://ci.example.org/runs/123", "type": "test_result", "description": "Public test result"},
            ],
            "milestone_proof",
            "Approve milestone",
        )

    def test_submit_evidence_pack(self):
        pack_id = self.graph.submit_evidence_pack(
            "A claim", "A clear claim description", [], "builder_submission"
        )
        self.assertEqual("pack_1", pack_id)

    def test_retrieve_evidence_pack(self):
        pack_id = self.graph.submit_evidence_pack(
            "A claim", "A clear claim description", [], "builder_submission"
        )
        pack = self.graph.get_evidence_pack(pack_id)
        self.assertEqual("A claim", pack["claim_title"])
        self.assertEqual("builder_submission", pack["target_use_case"])

    def test_review_weak_self_claim(self):
        pack_id = self.graph.submit_evidence_pack(
            "Trust me", "I completed everything.",
            [{"url": "", "type": "other", "description": "My own statement"}],
            "milestone_proof",
        )
        review = self.graph.review_evidence_pack(pack_id)
        self.assertLess(review["evidence_score"], 50)
        self.assertIn(review["verdict"], {"weak_evidence", "high_manipulation_risk", "needs_more_sources"})
        self.assertFalse(review["genlayer_ready"])

    def test_review_strong_milestone_evidence_pack(self):
        review = self.graph.review_evidence_pack(self._strong_pack())
        self.assertGreaterEqual(review["evidence_score"], 75)
        self.assertEqual("strong", review["source_quality"])
        self.assertEqual("evidence_ready", review["verdict"])
        self.assertTrue(review["genlayer_ready"])

    def test_total_score_equals_sub_score_sum(self):
        review = self.graph.review_evidence_pack(self._strong_pack())
        expected = sum(review[key] for key in (
            "completeness_score", "source_quality_score", "relevance_score",
            "manipulation_resistance_score", "genlayer_readiness_score",
        ))
        self.assertEqual(expected, review["evidence_score"])

    def test_verdict_changes_based_on_score_and_risk(self):
        weak_id = self.graph.submit_evidence_pack(
            "Unverified result", "I say this happened.",
            [{"url": "", "type": "screenshot", "description": "Untimestamped private screenshot"}],
            "dispute_evidence",
        )
        weak_review = self.graph.review_evidence_pack(weak_id)
        strong_review = self.graph.review_evidence_pack(self._strong_pack())
        self.assertNotEqual(weak_review["verdict"], strong_review["verdict"])
        self.assertNotEqual(weak_review["manipulation_risk"], strong_review["manipulation_risk"])

    def test_export_evidence_package_json(self):
        pack_id = self._strong_pack()
        exported = json.loads(self.graph.export_evidence_package(pack_id))
        self.assertEqual("evidencegraph.v1", exported["schema_version"])
        self.assertEqual(pack_id, exported["pack"]["pack_id"])
        self.assertEqual("evidence_ready", exported["contract_input"]["quality_gate"]["verdict"])
        self.assertNotIn("evidence_package_json", exported["review"])

    def test_pack_count_increments(self):
        self.assertEqual(0, self.graph.get_pack_count())
        self._strong_pack()
        self.assertEqual(1, self.graph.get_pack_count())

    def test_unknown_pack_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.graph.get_evidence_pack("pack_404")


if __name__ == "__main__":
    unittest.main()
