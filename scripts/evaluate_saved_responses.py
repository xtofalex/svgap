#!/usr/bin/env python3
"""Evaluate saved taskpack responses separately from credentialed generation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--responses",
        type=Path,
        required=True,
        help="directory containing <run-id>/<task>.txt response files",
    )
    parser.add_argument("--task-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    response_root = args.responses.resolve()
    task_root = args.task_root.resolve()
    output = args.output.resolve()
    responses = sorted(response_root.glob("*/*.txt"))
    if not responses:
        parser.error(f"no response files found under {response_root}")
    failures = 0
    for response in responses:
        run_id = response.parent.name
        task_id = response.stem
        metadata_path = response.with_suffix(".generation.json")
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            label = metadata["configuration_label"]
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            print(f"METADATA_ERROR {run_id}/{task_id}: {exc}", file=sys.stderr)
            failures += 1
            continue
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "svgap",
                "pilot",
                str(task_root / task_id),
                str(response),
                "--model",
                str(label),
                "--run-id",
                run_id,
                "--output",
                str(output),
            ],
            check=False,
            text=True,
        )
        run_dir = output / run_id / task_id
        if run_dir.is_dir():
            shutil.copy2(metadata_path, run_dir / "generation.json")
        if completed.returncode not in (0, 1, 3):
            failures += 1
    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
