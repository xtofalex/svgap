#!/usr/bin/env python3
"""Run diagnosis or repair starters through a provider-neutral command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

from svgap.challenge import ChallengeError, score_challenge


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "challenges/v0.1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("track", choices=("diagnosis", "repair"))
    parser.add_argument("--command", required=True, help="reads prompt on stdin; writes response")
    parser.add_argument("--label", required=True, help="stable public configuration label")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error(f"refusing to overwrite output directory: {output}")
    output.mkdir(parents=True)
    try:
        if args.track == "diagnosis":
            run_diagnosis(args.command, args.label, args.run_id, output)
        else:
            run_repair(args.command, args.label, args.run_id, output)
    except (OSError, ValueError, subprocess.SubprocessError, ChallengeError) as exc:
        print(f"challenge run failed: {exc}", file=sys.stderr)
        return 2
    return 0


def run_diagnosis(command: str, label: str, run_id: str, output: Path) -> None:
    root = PACK / "diagnosis"
    raw = run_model(command, (root / "prompt.md").read_text(encoding="utf-8"))
    (output / "raw-response.txt").write_text(raw, encoding="utf-8")
    payload = extract_json(raw)
    responses = payload.get("responses") if isinstance(payload, dict) else None
    if not isinstance(responses, list):
        raise ValueError("diagnosis response must be a JSON object with a responses array")
    submission = {
        "schema_version": "1.0",
        "challenge_id": "frontier-model-handoff-v0.1",
        "task_id": "diagnose-production-evidence",
        "model": label,
        "run_id": run_id,
        "responses": responses,
    }
    write_and_score(root / "task.json", submission, output)


def run_repair(command: str, label: str, run_id: str, output: Path) -> None:
    root = PACK / "repair"
    starter = root / "starter"
    prompt = (root / "prompt.md").read_text(encoding="utf-8")
    unsafe = (starter / "before.sv").read_text(encoding="utf-8")
    raw = run_model(command, f"{prompt}\n\nUnsafe module:\n```systemverilog\n{unsafe}```\n")
    (output / "raw-response.txt").write_text(raw, encoding="utf-8")
    after_response = output / "after-response.txt"
    after_response.write_text(raw, encoding="utf-8")
    work = output / "work"
    before = evaluate(starter, starter / "before.sv", "starter-input", "before", work)
    after = evaluate(starter, after_response, label, "after", work)
    shutil.copy2(before, output / "before-report.json")
    shutil.copy2(after, output / "after-report.json")
    submission = {
        "schema_version": "1.0",
        "challenge_id": "frontier-model-handoff-v0.1",
        "task_id": "repair-reset-domain-finding",
        "model": label,
        "run_id": run_id,
        "artifacts": {
            "before_report": "before-report.json",
            "after_report": "after-report.json",
        },
    }
    write_and_score(root / "task.json", submission, output)


def run_model(command: str, prompt: str) -> str:
    completed = subprocess.run(
        command,
        shell=True,
        input=prompt,
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if completed.returncode:
        raise subprocess.SubprocessError(completed.stderr[-4000:])
    if not completed.stdout.strip():
        raise subprocess.SubprocessError("model command produced empty stdout")
    return completed.stdout


def extract_json(text: str) -> dict[str, object]:
    fenced = re.findall(r"```(?:json)?\s*(.*?)```", text, re.I | re.S)
    candidates = [*fenced, text]
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            return payload
    raise ValueError("model response does not contain a JSON object")


def evaluate(task: Path, response: Path, label: str, run_id: str, output: Path) -> Path:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "svgap",
            "pilot",
            str(task),
            str(response),
            "--model",
            label,
            "--run-id",
            run_id,
            "--output",
            str(output),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode not in (0, 1, 3):
        raise subprocess.SubprocessError(completed.stderr[-4000:])
    report = output / run_id / "repair-reset-release" / "report.json"
    if not report.is_file():
        raise OSError(f"evaluation report was not written: {report}")
    return report


def write_and_score(task: Path, submission: dict[str, object], output: Path) -> None:
    submission_path = output / "submission.json"
    submission_path.write_text(
        json.dumps(submission, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    result = score_challenge(task, submission_path)
    (output / "result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"track       {result['track']}")
    print(f"overall     {result['overall']}")
    print(f"result      {output / 'result.json'}")


if __name__ == "__main__":
    raise SystemExit(main())
