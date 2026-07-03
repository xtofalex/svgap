#!/usr/bin/env python3
"""Verify hashes and normalized outcomes in the public reset artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from svgap.provenance import canonical_file_set_digest


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT = ROOT / "artifacts/reset-replication-v0.1"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", nargs="?", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args()
    artifact = args.artifact.resolve()
    manifest = json.loads((artifact / "manifest.json").read_text(encoding="utf-8"))
    candidates = manifest["candidates"]
    if manifest["candidate_count"] != len(candidates):
        raise SystemExit("manifest candidate_count does not match index length")

    for item in candidates:
        directory = artifact / "candidates" / item["run_id"] / item["task_id"]
        provenance = json.loads(
            (directory / "provenance.json").read_text(encoding="utf-8")
        )
        files = [directory / name for name in provenance["files"]]
        for path in files:
            if not path.is_file():
                raise SystemExit(f"missing artifact file: {path}")
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != provenance["files"][path.name]:
                raise SystemExit(f"hash mismatch: {path}")
        bundle = canonical_file_set_digest(directory, files)
        if bundle != provenance["candidate_bundle_digest"]:
            raise SystemExit(f"candidate bundle mismatch: {directory}")
        if bundle != item["bundle_digest"]:
            raise SystemExit(f"index bundle mismatch: {directory}")
        report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
        if report["functional"]["status"] != item["functional"]:
            raise SystemExit(f"functional status mismatch: {directory}")
        if report["structural"]["status"] != item["structural"]:
            raise SystemExit(f"structural status mismatch: {directory}")

    print(f"verified     {len(candidates)} candidates")
    print(f"artifact     {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
