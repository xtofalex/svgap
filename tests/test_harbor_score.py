from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]
SCORE_PATH = (
    ROOT
    / "integrations"
    / "harbor"
    / "svgap-reset-release"
    / "reset-counter"
    / "tests"
    / "score.py"
)


def load_score_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("harbor_svgap_score", SCORE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCORE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCORE = load_score_module()


class HarborScoreTests(TestCase):
    def test_safe_candidate_receives_primary_reward(self) -> None:
        rewards, verdict = SCORE.score_report(
            report("pass", "pass", gap_member=False)
        )
        self.assertEqual(rewards["reward"], 1)
        self.assertEqual(rewards["functional_accept"], 1)
        self.assertEqual(rewards["structural_accept"], 1)
        self.assertFalse(verdict["gap_member"])

    def test_gap_candidate_preserves_paired_metrics(self) -> None:
        rewards, verdict = SCORE.score_report(
            report("pass", "fail", gap_member=True)
        )
        self.assertEqual(rewards["reward"], 0)
        self.assertEqual(rewards["functional_accept"], 1)
        self.assertEqual(rewards["structural_accept"], 0)
        self.assertEqual(rewards["gap_member"], 1)
        self.assertTrue(verdict["gap_member"])

    def test_unknown_is_non_passing(self) -> None:
        rewards, verdict = SCORE.score_report(report("pass", "unknown"))
        self.assertEqual(rewards["reward"], 0)
        self.assertEqual(rewards["unknown"], 1)
        self.assertTrue(verdict["unknown"])

    def test_tool_error_is_non_passing(self) -> None:
        rewards, verdict = SCORE.score_report(report("pass", "tool_error"))
        self.assertEqual(rewards["reward"], 0)
        self.assertEqual(rewards["tool_error"], 1)
        self.assertTrue(verdict["tool_error"])


def report(
    functional: str, structural: str, *, gap_member: bool = False
) -> dict[str, object]:
    return {
        "functional": {"status": functional},
        "structural": {"status": structural},
        "gap_member": gap_member,
    }
