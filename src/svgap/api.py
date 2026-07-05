"""Library entry point for evaluating candidates programmatically.

The CLI and this module share one evaluation path. Setup problems (a broken
manifest, an unknown backend) raise; measurement outcomes — including
``unknown`` and ``tool_error`` — are returned inside the report, never raised.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from svgap.backends.registry import load_backend
from svgap.functional import run_functional
from svgap.manifest import Manifest, load_manifest
from svgap.model import EvaluationReport, FunctionalResult


def evaluate(
    manifest: Manifest | str | Path,
    *,
    skip_functional: bool = False,
    write_report: bool = True,
    manifest_label: str | None = None,
) -> EvaluationReport:
    """Evaluate one RTL candidate and return its layered report.

    ``manifest`` is a loaded :class:`Manifest` or a path to one. When
    ``write_report`` is true (the default, matching ``svgap check``), the
    schema-versioned report is atomically written to the manifest's report
    path. ``manifest_label`` overrides the manifest path recorded inside the
    report, for callers that need portable paths.
    """
    if not isinstance(manifest, Manifest):
        manifest = load_manifest(Path(manifest))
    functional = (
        FunctionalResult(status="not_run") if skip_functional else run_functional(manifest)
    )
    backend = load_backend(manifest.backend)
    structural = backend.check(manifest)
    report = EvaluationReport(
        schema_version="1.0",
        candidate_id=manifest.candidate_id,
        manifest=manifest_label or str(manifest.path),
        functional=functional,
        structural=structural,
        gap_member=functional.status == "pass" and structural.status == "fail",
        generated_at=datetime.now(timezone.utc).isoformat(),
    )
    if write_report:
        manifest.report_path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(report.to_dict(), indent=2, sort_keys=True)
        temporary = manifest.report_path.with_suffix(manifest.report_path.suffix + ".tmp")
        temporary.write_text(payload + "\n", encoding="utf-8")
        temporary.replace(manifest.report_path)
    return report
