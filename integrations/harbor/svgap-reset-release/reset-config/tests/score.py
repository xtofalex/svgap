#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--reward", type=Path, required=True)
    parser.add_argument("--verdict", type=Path, required=True)
    args = parser.parse_args()

    report: dict[str, Any] | None = None
    diagnostic = "report_missing"
    if args.report and args.report.is_file():
        try:
            report = json.loads(args.report.read_text(encoding="utf-8"))
            diagnostic = ""
        except (OSError, json.JSONDecodeError):
            diagnostic = "report_invalid"

    rewards, verdict = score_report(report, diagnostic)
    args.reward.parent.mkdir(parents=True, exist_ok=True)
    args.verdict.parent.mkdir(parents=True, exist_ok=True)
    args.reward.write_text(
        json.dumps(rewards, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    args.verdict.write_text(
        json.dumps(verdict, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 0


def score_report(
    report: dict[str, Any] | None, diagnostic: str = ""
) -> tuple[dict[str, int], dict[str, Any]]:
    functional_status = status(report, "functional")
    structural_status = status(report, "structural")
    functional_accept = int(functional_status == "pass")
    structural_accept = int(structural_status == "pass")
    gap_member = int(bool(report and report.get("gap_member")))
    unknown = int(
        functional_status in {"unknown", "not_run"}
        or structural_status in {"unknown", "not_run"}
    )
    tool_error = int("tool_error" in {functional_status, structural_status})
    primary_reward = int(functional_accept == 1 and structural_accept == 1)

    rewards = {
        "reward": primary_reward,
        "functional_accept": functional_accept,
        "structural_accept": structural_accept,
        "gap_member": gap_member,
        "unknown": unknown,
        "tool_error": tool_error,
    }
    verdict = {
        "schema_version": "harbor-svgap-1.0",
        "functional_status": functional_status,
        "structural_status": structural_status,
        "gap_member": bool(gap_member),
        "unknown": bool(unknown),
        "tool_error": bool(tool_error),
        "primary_reward": primary_reward,
        "diagnostic": diagnostic,
        "claim_boundary": (
            "Results are conditional on supplied functional evidence and the "
            "configured structural rule. They are not silicon signoff."
        ),
    }
    return rewards, verdict


def status(report: dict[str, Any] | None, layer: str) -> str:
    if not report:
        return "not_run"
    value = report.get(layer)
    if not isinstance(value, dict):
        return "unknown"
    return str(value.get("status", "unknown"))


if __name__ == "__main__":
    raise SystemExit(main())
