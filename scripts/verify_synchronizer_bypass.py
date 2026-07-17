"""Verify the synchronizer-bypass pattern in the frozen reset artifact.

For every gap case in artifacts/reset-replication-v0.1 (functional pass with
a REF-RDC-001 finding), this checks that the same design also contains a
two-flop reset synchronizer recognized by the reference oracle. That is the
documented qualitative pattern: the model builds the textbook synchronizer
and wires the raw asynchronous reset past it.

The artifact is read-only for this script: the Yosys netlist is written to a
temporary directory, never into the frozen candidate tree.

Usage: python scripts/verify_synchronizer_bypass.py
Exit code 0 when every gap case contains a recognized synchronizer.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from svgap.backends.reference_yosys import (  # noqa: E402
    SeqCell,
    first,
    is_sequential,
    reset_synchronizer_bits,
    yosys_quote,
)
from svgap.manifest import load_manifest  # noqa: E402

ARTIFACT = Path(__file__).resolve().parents[1] / "artifacts" / "reset-replication-v0.1"


def contains_recognized_synchronizer(manifest_path: Path) -> bool:
    manifest = load_manifest(manifest_path)
    with tempfile.TemporaryDirectory() as tmp:
        netlist_path = Path(tmp) / "structural.json"
        script = "\n".join(
            [
                *[f"read_verilog -sv {yosys_quote(path)}" for path in manifest.sources],
                f"hierarchy -check -top {manifest.top}",
                "proc",
                "opt_clean",
                f"write_json {yosys_quote(netlist_path)}",
            ]
        )
        completed = subprocess.run(
            ["yosys", "-q", "-p", script],
            cwd=manifest.path.parent,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"yosys failed for {manifest_path}: "
                f"{completed.stderr.strip() or completed.stdout.strip()}"
            )
        module = json.loads(netlist_path.read_text(encoding="utf-8"))["modules"][
            manifest.top
        ]

    port_bits = {
        name: tuple(data.get("bits", ()))
        for name, data in module.get("ports", {}).items()
    }
    reset_by_bit = {}
    for reset in manifest.resets:
        bits = port_bits.get(reset.port, ())
        if len(bits) == 1:
            reset_by_bit[bits[0]] = reset

    seq: list[SeqCell] = []
    for name, cell in module.get("cells", {}).items():
        if not is_sequential(cell.get("type", "")):
            continue
        connections = cell.get("connections", {})
        clk = first(connections.get("CLK", ()))
        seq.append(
            SeqCell(
                name=name,
                cell_type=cell.get("type", ""),
                clock_bit=clk,
                clock_name="",
                d_bits=tuple(connections.get("D", ())),
                q_bits=tuple(connections.get("Q", ())),
                arst_bits=tuple(connections.get("ARST", ())),
                attributes=cell.get("attributes", {}),
                srst_bits=tuple(connections.get("SRST", ())),
            )
        )
    return bool(reset_synchronizer_bits(seq, reset_by_bit))


def main() -> int:
    index = json.loads((ARTIFACT / "manifest.json").read_text(encoding="utf-8"))
    per_config: dict[str, dict[str, int]] = defaultdict(
        lambda: {"gap": 0, "with_synchronizer": 0}
    )
    missing: list[str] = []

    for item in index["candidates"]:
        directory = ARTIFACT / "candidates" / item["run_id"] / item["task_id"]
        report = json.loads((directory / "report.json").read_text(encoding="utf-8"))
        is_gap = report["functional"]["status"] == "pass" and any(
            finding["rule_id"] == "REF-RDC-001"
            for finding in report["structural"]["findings"]
        )
        if not is_gap:
            continue
        config = item["run_id"].rsplit("--", 1)[0]
        per_config[config]["gap"] += 1
        if contains_recognized_synchronizer(directory / "manifest.toml"):
            per_config[config]["with_synchronizer"] += 1
        else:
            missing.append(f"{item['run_id']}/{item['task_id']}")

    total_gap = sum(v["gap"] for v in per_config.values())
    total_with = sum(v["with_synchronizer"] for v in per_config.values())
    for config, counts in sorted(per_config.items()):
        print(
            f"{config:24} gap cases {counts['gap']:2}  "
            f"with recognized synchronizer {counts['with_synchronizer']:2}"
        )
    print(f"{'total':24} gap cases {total_gap:2}  with recognized synchronizer {total_with:2}")

    if missing:
        print("gap cases without a recognized synchronizer:", file=sys.stderr)
        for case in missing:
            print(f"  {case}", file=sys.stderr)
        return 1
    if total_gap != 14:
        print(f"expected 14 gap cases in the frozen artifact, found {total_gap}", file=sys.stderr)
        return 1
    print("verified: every gap case also contains a recognized reset synchronizer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
