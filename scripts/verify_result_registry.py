#!/usr/bin/env python3
"""Validate the public result registry and every file reference it contains."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from svgap.submission import validate_submission


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    registry_path = ROOT / "results" / "registry-v1.json"
    schema = json.loads((ROOT / "schemas" / "result-registry-v1.json").read_text())
    registry = json.loads(registry_path.read_text())
    Draft202012Validator(schema).validate(registry)
    for track in ("diagnosis", "repair"):
        for entry in registry[track]:
            for field in ("result", "submission", "provenance"):
                path = ROOT / entry[field]
                if not path.is_file():
                    raise SystemExit(f"missing {field}: {path}")
    for entry in registry["submissions"]:
        directory = ROOT / entry["source"]
        manifest, _ = validate_submission(directory)
        if manifest["submission_id"] != entry["submission_id"]:
            raise SystemExit(f"submission id mismatch: {directory}")
    print(f"valid: {registry_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
