"""Deterministic local evidence scoring for the EvidenceGraph MVP."""

from copy import deepcopy
from datetime import datetime, timezone
from urllib.parse import urlparse
import json


class EvidenceGraph:
    """Store, review, and export evidence packs in memory."""

    TYPE_QUALITY = {
        "github_repo": 5,
        "commit_release": 6,
        "demo_video": 4,
        "documentation": 5,
        "test_result": 5,
        "screenshot": 2,
        "transaction_hash": 6,
        "article_source": 4,
        "api_log": 4,
        "other": 1,
    }
    USE_CASE_EVIDENCE = {
        "builder_submission": {"github_repo", "documentation", "demo_video", "test_result"},
        "milestone_proof": {"github_repo", "commit_release", "demo_video", "test_result", "transaction_hash"},
        "dispute_evidence": {"documentation", "screenshot", "transaction_hash", "article_source", "api_log"},
        "agent_sla_claim": {"test_result", "transaction_hash", "api_log"},
        "grant_proposal": {"github_repo", "documentation", "demo_video", "article_source"},
        "prediction_resolver": {"transaction_hash", "article_source", "api_log"},
        "other": set(TYPE_QUALITY),
    }
    HARD_TO_FAKE = {"commit_release", "test_result", "transaction_hash", "api_log"}
    TIMESTAMPED = {"commit_release", "test_result", "transaction_hash", "api_log"}

    def __init__(self):
        self._packs = {}
        self._reviews = {}

    def submit_evidence_pack(self, claim_title, claim_description, evidence_items,
                             target_use_case, expected_outcome=""):
        pack_id = f"pack_{len(self._packs) + 1}"
        normalized_items = [self._normalize_item(item) for item in (evidence_items or [])]
        self._packs[pack_id] = {
            "pack_id": pack_id,
            "claim_title": str(claim_title or "").strip(),
            "claim_description": str(claim_description or "").strip(),
            "evidence_items": normalized_items,
            "target_use_case": str(target_use_case or "other").strip(),
            "expected_outcome": str(expected_outcome or "").strip(),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
        }
        return pack_id

    def review_evidence_pack(self, pack_id):
        pack = self._require_pack(pack_id)
        items = pack["evidence_items"]
        public_items = [item for item in items if self._is_public_url(item["url"])]
        domains = {urlparse(item["url"]).netloc.lower() for item in public_items}
        independent = len(domains) >= 2

        completeness = (
            (5 if pack["claim_title"] else 0)
            + (5 if len(pack["claim_description"]) >= 20 else 2 if pack["claim_description"] else 0)
            + (8 if len(items) >= 2 else 3 if items else 0)
            + (6 if independent else 2 if public_items else 0)
            + (6 if self._has_relevant_evidence(pack) else 0)
        )
        source_quality = min(25, sum(
            self.TYPE_QUALITY.get(item["type"], 1) if item["url"] else 0 for item in items
        ))
        matching_count = sum(
            item["type"] in self.USE_CASE_EVIDENCE.get(pack["target_use_case"], set())
            for item in items
        )
        relevance = min(20,
            (5 if len(pack["claim_description"]) >= 20 else 2 if pack["claim_description"] else 0)
            + (5 if pack["target_use_case"] else 0)
            + min(10, matching_count * 2)
        )
        manipulation_resistance = (
            (3 if public_items else 0)
            + (4 if any(item["type"] in self.TIMESTAMPED for item in public_items) else 0)
            + (4 if independent else 0)
            + (4 if any(item["type"] in self.HARD_TO_FAKE for item in public_items) else 0)
        )
        genlayer_readiness = (
            3  # This review always produces structured, contract-consumable JSON.
            + (3 if pack["target_use_case"] in self.USE_CASE_EVIDENCE else 0)
            + (2 if pack["claim_description"] else 0)
            + (2 if len(items) >= 2 else 0)
        )
        total = completeness + source_quality + relevance + manipulation_resistance + genlayer_readiness
        risk = "low" if manipulation_resistance >= 12 else "medium" if manipulation_resistance >= 7 else "high"
        source_label = "strong" if source_quality >= 19 else "moderate" if source_quality >= 10 else "weak"
        genlayer_ready = genlayer_readiness >= 8 and total >= 60 and len(items) >= 2
        missing = self._missing_evidence(pack, independent)
        verdict = self._verdict(total, risk, genlayer_ready, len(items), source_quality)

        # Future GenLayer integration point: ask an LLM to assess semantic relevance
        # and use web access to verify live URLs before finalizing these heuristics.
        review = {
            "pack_id": pack_id,
            "evidence_score": total,
            "completeness_score": completeness,
            "source_quality_score": source_quality,
            "relevance_score": relevance,
            "manipulation_resistance_score": manipulation_resistance,
            "genlayer_readiness_score": genlayer_readiness,
            "source_quality": source_label,
            "manipulation_risk": risk,
            "genlayer_ready": genlayer_ready,
            "verdict": verdict,
            "missing_evidence": missing,
            "recommendation": self._recommendation(verdict, missing),
        }
        review["evidence_package_json"] = json.dumps(
            self._package_payload(pack, review), indent=2, sort_keys=True
        )
        self._reviews[pack_id] = review
        return deepcopy(review)

    def get_evidence_pack(self, pack_id):
        return deepcopy(self._require_pack(pack_id))

    def get_review(self, pack_id):
        if pack_id not in self._reviews:
            self.review_evidence_pack(pack_id)
        return deepcopy(self._reviews[pack_id])

    def get_pack_count(self):
        return len(self._packs)

    def export_evidence_package(self, pack_id):
        review = self.get_review(pack_id)
        return review["evidence_package_json"]

    @staticmethod
    def _package_payload(pack, review):
        clean_review = {key: value for key, value in review.items() if key != "evidence_package_json"}
        return {
            "schema_version": "evidencegraph.v1",
            "pack": pack,
            "review": clean_review,
            "contract_input": {
                "claim": {
                    "title": pack["claim_title"],
                    "description": pack["claim_description"],
                    "expected_outcome": pack["expected_outcome"],
                },
                "target_use_case": pack["target_use_case"],
                "evidence": pack["evidence_items"],
                "quality_gate": {
                    "score": clean_review["evidence_score"],
                    "verdict": clean_review["verdict"],
                    "manipulation_risk": clean_review["manipulation_risk"],
                    "genlayer_ready": clean_review["genlayer_ready"],
                },
            },
        }

    def _require_pack(self, pack_id):
        if pack_id not in self._packs:
            raise KeyError(f"Unknown evidence pack: {pack_id}")
        return self._packs[pack_id]

    @staticmethod
    def _normalize_item(item):
        item = item if isinstance(item, dict) else {}
        return {
            "url": str(item.get("url", "")).strip(),
            "type": str(item.get("type", "other")).strip() or "other",
            "description": str(item.get("description", "")).strip(),
        }

    @staticmethod
    def _is_public_url(url):
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

    def _has_relevant_evidence(self, pack):
        relevant = self.USE_CASE_EVIDENCE.get(pack["target_use_case"], set())
        return any(item["type"] in relevant and item["url"] for item in pack["evidence_items"])

    def _missing_evidence(self, pack, independent):
        missing = []
        if not pack["claim_title"]:
            missing.append("Claim title")
        if len(pack["claim_description"]) < 20:
            missing.append("A clear, detailed claim description")
        if len(pack["evidence_items"]) < 2:
            missing.append("At least two evidence items")
        if not independent:
            missing.append("An independent source on a different public domain")
        if not self._has_relevant_evidence(pack):
            missing.append("Evidence matched to the selected GenLayer use case")
        if not any(item["type"] in self.TIMESTAMPED and item["url"] for item in pack["evidence_items"]):
            missing.append("Timestamped proof such as a release, test run, transaction, or log")
        return missing

    @staticmethod
    def _verdict(total, risk, ready, item_count, source_quality):
        if risk == "high" and item_count > 0:
            return "high_manipulation_risk"
        if not ready and total >= 50:
            return "not_genlayer_ready"
        if item_count < 2:
            return "needs_more_sources"
        if source_quality < 10 or total < 50:
            return "weak_evidence"
        return "evidence_ready" if total >= 75 else "needs_more_sources"

    @staticmethod
    def _recommendation(verdict, missing):
        if verdict == "evidence_ready":
            return "Package is ready for Intelligent Contract review; preserve source URLs and timestamps."
        if missing:
            return "Add: " + "; ".join(missing[:3]) + "."
        return "Add stronger public, timestamped, and independently verifiable evidence."
