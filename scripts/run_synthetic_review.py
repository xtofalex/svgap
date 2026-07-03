#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
TARGET_PACKET = ROOT / "review_packets/reset-replication-v0.3/cases"
CALIBRATION_PACKET = ROOT / "review_packets/synthetic-calibration-v0.1/cases"
SCHEMA_PATH = ROOT / "schemas/synthetic-review-v1.json"
DEFAULT_OUTPUT = ROOT / "reports/generated/synthetic-review-v0.1"


RUBRIC = """You are a blinded RTL reset-domain adjudicator. Review exactly one case.

Primary question: Does any ordinary operational state element—not a reset
synchronizer stage itself—use the external raw asynchronous reset (or a trivial
alias of it) on its asynchronous reset input, allowing raw reset removal to reach
that state directly despite the requested synchronized-release path?

Decision rules:
- YES: ordinary state directly uses the raw reset or a trivial alias, even if
  synchronous logic also holds the state reset for extra cycles.
- NO: raw reset is used only by reset-synchronizer stages, while operational
  state uses a derived synchronized/local reset or a clocked reset condition.
- UNCERTAIN: hierarchy, complex gating, or missing information prevents a firm
  structural decision.
- Comments and signal names are not proof. Inspect sensitivity/event controls
  and assignments.
- Do not assess general design quality, functionality, or silicon failure.
- Cite the numbered Candidate RTL lines that establish the decision.

Return only an object matching the supplied JSON schema. Do not mention model
identity, automated tools, prior verdicts, or other cases.

CASE FOLLOWS
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("provider", choices=("codex", "claude"))
    parser.add_argument("--model", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument("--repeat", type=int, choices=(1, 2), required=True)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--retry-complete",
        action="store_true",
        help="regenerate cases that already have a validated JSON judgment",
    )
    args = parser.parse_args()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    cases = sorted([*TARGET_PACKET.glob("*.md"), *CALIBRATION_PACKET.glob("*.md")])
    if args.limit:
        cases = cases[: args.limit]
    output = args.output.resolve() / args.label / f"repeat-{args.repeat:02d}"
    output.mkdir(parents=True, exist_ok=True)
    failures = []
    with tempfile.TemporaryDirectory(prefix="svgap-review-") as sandbox_name:
        sandbox = Path(sandbox_name)
        for index, case_path in enumerate(cases, 1):
            case_id = case_path.stem
            numbered_case, rtl_lines = number_candidate_rtl(
                case_path.read_text(encoding="utf-8")
            )
            result_path = output / f"{case_id}.json"
            if result_path.exists() and not args.retry_complete:
                try:
                    existing = json.loads(result_path.read_text(encoding="utf-8"))
                    errors = list(validator.iter_errors(existing))
                    if errors:
                        raise ValueError(errors[0].message)
                    if any(
                        line < 1 or line > rtl_lines
                        for line in existing["evidence_lines"]
                    ):
                        raise ValueError("stored evidence line is outside candidate RTL")
                    if not existing["evidence_lines"]:
                        raise ValueError("stored judgment has no RTL evidence lines")
                    print(f"[{index:03d}/{len(cases):03d}] SKIP {case_id}")
                    continue
                except (ValueError, json.JSONDecodeError):
                    result_path.unlink(missing_ok=True)
                    (output / f"{case_id}.raw.txt").unlink(missing_ok=True)
            prompt = RUBRIC + numbered_case
            try:
                raw, result = generate(
                    args.provider, args.model, prompt, schema, sandbox
                )
                result = normalize_result(result)
                errors = list(validator.iter_errors(result))
                if errors:
                    raise ValueError(errors[0].message)
                invalid_lines = [
                    line for line in result["evidence_lines"]
                    if line < 1 or line > rtl_lines
                ]
                if invalid_lines:
                    raise ValueError(
                        f"evidence lines outside 1..{rtl_lines}: {invalid_lines}"
                    )
                if not result["evidence_lines"]:
                    raise ValueError("review judgment has no RTL evidence lines")
            except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
                failures.append({"case_id": case_id, "error": str(exc)})
                print(f"[{index:03d}/{len(cases):03d}] ERROR {case_id}: {exc}")
                continue
            result_path.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            (output / f"{case_id}.raw.txt").write_text(raw, encoding="utf-8")
            print(
                f"[{index:03d}/{len(cases):03d}] {case_id} "
                f"{result['decision']} {result['confidence']}"
            )
    metadata = {
        "schema_version": "1.0",
        "provider": args.provider,
        "model": args.model,
        "label": args.label,
        "repeat": args.repeat,
        "interface_version": provider_version(args.provider),
        "rubric_sha256": hashlib.sha256(RUBRIC.encode()).hexdigest(),
        "schema_sha256": hashlib.sha256(SCHEMA_PATH.read_bytes()).hexdigest(),
        "case_count": len(cases),
        "completed_count": len(cases) - len(failures),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "failures": failures,
    }
    (output / "metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return 2 if failures else 0


def number_candidate_rtl(case_text: str) -> tuple[str, int]:
    matches = list(re.finditer(r"```systemverilog\n(.*?)```", case_text, re.S))
    if not matches:
        raise ValueError("case has no SystemVerilog block")
    match = matches[-1]
    lines = match.group(1).rstrip().splitlines()
    numbered = "\n".join(f"{index:4d} | {line}" for index, line in enumerate(lines, 1))
    return case_text[: match.start(1)] + numbered + "\n" + case_text[match.end(1) :], len(lines)


def generate(
    provider: str,
    model: str,
    prompt: str,
    schema: dict[str, object],
    sandbox: Path,
) -> tuple[str, dict[str, object]]:
    if provider == "codex":
        binary = require_executable("codex")
        output = sandbox / "last-message.json"
        command = [
            binary,
            "--ask-for-approval",
            "never",
            "exec",
            "--ephemeral",
            "--ignore-user-config",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--model",
            model,
            "-c",
            f'model_reasoning_effort="{codex_effort(model)}"',
            "--cd",
            str(sandbox),
            "--output-schema",
            str(SCHEMA_PATH),
            "--output-last-message",
            str(output),
            prompt,
        ]
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=600, check=False
        )
        if completed.returncode:
            raise subprocess.SubprocessError(completed.stderr[-4000:])
        raw = output.read_text(encoding="utf-8")
        return raw, json.loads(raw)

    binary = require_executable("claude")
    command = [
        binary,
        "--print",
        "--bare",
        "--tools",
        "",
        "--no-session-persistence",
        "--model",
        model,
        "--effort",
        "max",
        "--json-schema",
        json.dumps(schema, separators=(",", ":")),
        "--output-format",
        "json",
        prompt,
    ]
    completed = subprocess.run(
        command,
        cwd=sandbox,
        env=os.environ.copy(),
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if completed.returncode:
        raise subprocess.SubprocessError(completed.stderr[-4000:])
    if not completed.stdout.strip():
        raise subprocess.SubprocessError(
            "Claude returned empty stdout: " + completed.stderr[-4000:]
        )
    try:
        envelope = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Claude returned non-JSON output: {completed.stdout[-2000:]} "
            f"stderr: {completed.stderr[-2000:]}"
        ) from exc
    result = envelope.get("structured_output")
    if result is None:
        value = envelope.get("result")
        if isinstance(value, str):
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", value.strip(), flags=re.I)
            try:
                result = json.loads(cleaned)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Claude result was not a JSON object: {value[-2000:]}"
                ) from exc
        else:
            result = value
    if not isinstance(result, dict):
        raise ValueError("Claude response did not contain structured output")
    return completed.stdout, result


def require_executable(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        raise OSError(f"required reviewer CLI is not on PATH: {name}")
    return path


def normalize_result(result: dict[str, object]) -> dict[str, object]:
    """Normalize provider structured-output aliases without changing decisions."""
    decision = first_decision(result)
    evidence = first_evidence_lines(result)
    reasoning = first_text(
        result,
        (
            "reasoning_summary",
            "rationale",
            "reasoning",
            "justification",
            "analysis",
            "notes",
            "comments",
            "supporting_detail",
            "decision_basis",
        ),
    )
    if not reasoning:
        reasoning = "Structured judgment supplied without a separate rationale."
    confidence = first_text(result, ("confidence",)).lower()
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"
    return {
        "decision": decision,
        "confidence": confidence,
        "raw_reset_signal": first_text(
            result, ("raw_reset_signal", "external_reset", "reset_signal")
        ),
        "operational_state": first_string_list(
            result,
            ("operational_state", "operational_elements", "primary_elements"),
        ),
        "reset_synchronizer_state": first_string_list(
            result,
            ("reset_synchronizer_state", "synchronizer_state"),
        ),
        "evidence_lines": evidence,
        "reasoning_summary": reasoning[:1200],
    }


def codex_effort(model: str) -> str:
    return "xhigh" if model == "gpt-5.5" else "max"


def first_decision(result: dict[str, object]) -> str:
    preferred = (
        "decision",
        "verdict",
        "answer",
        "conclusion",
        "primary_question_answer",
        "decision_category",
        "primary_question",
    )
    for key in preferred:
        value = result.get(key)
        decision = decision_from_value(value)
        if decision:
            return decision
    for value in result.values():
        decision = decision_from_value(value)
        if decision:
            return decision
    raise ValueError("review response has no unambiguous yes/no/uncertain decision")


def decision_from_value(value: object) -> str:
    if isinstance(value, bool):
        return "yes" if value else "no"
    if not isinstance(value, str):
        return ""
    match = re.search(r"\b(yes|no|uncertain)\b", value, re.I)
    return match.group(1).lower() if match else ""


def first_evidence_lines(result: dict[str, object]) -> list[int]:
    exact = (
        "evidence_lines",
        "cited_lines",
        "line_citations",
        "citations",
        "key_lines",
        "supporting_lines",
        "decision_lines",
        "critical_lines",
        "citing_lines",
        "lines",
        "cite",
        "primary_evidence",
        "key_evidence",
        "evidence",
    )
    for key in exact:
        if key in result:
            lines = parse_line_numbers(result[key])
            if lines:
                return lines
    return []


def parse_line_numbers(value: object) -> list[int]:
    if isinstance(value, int) and not isinstance(value, bool):
        return [value] if value >= 1 else []
    if isinstance(value, list):
        lines: list[int] = []
        for item in value:
            lines.extend(parse_line_numbers(item))
        return sorted(set(lines))
    if isinstance(value, dict):
        lines = []
        for item in value.values():
            lines.extend(parse_line_numbers(item))
        return sorted(set(lines))
    if not isinstance(value, str):
        return []
    lines = []
    for start, end in re.findall(r"(?<![A-Za-z0-9_])(\d+)(?:\s*[-–:]\s*(\d+))?", value):
        first = int(start)
        last = int(end) if end else first
        if first >= 1 and last >= first and last - first <= 20:
            lines.extend(range(first, last + 1))
    return sorted(set(lines))


def first_text(result: dict[str, object], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = result.get(key)
        if isinstance(value, str):
            return value.strip()
    return ""


def first_string_list(
    result: dict[str, object], keys: tuple[str, ...]
) -> list[str]:
    for key in keys:
        value = result.get(key)
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
    return []


def provider_version(provider: str) -> str:
    binary = require_executable("codex" if provider == "codex" else "claude")
    completed = subprocess.run(
        [binary, "--version"], capture_output=True, text=True, timeout=30, check=False
    )
    return (completed.stdout.strip() or completed.stderr.strip() or "unknown").splitlines()[-1]


if __name__ == "__main__":
    raise SystemExit(main())
