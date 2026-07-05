import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from svgap.submission import (
    SubmissionError,
    bundle_submission,
    initialize_submission,
    validate_submission,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "challenges/v0.1/generation/report.json"
DIAGNOSIS_RESULT = ROOT / "results/baselines/v0.1/diagnosis/gpt-5.4/result.json"


class SubmissionTests(TestCase):
    def initialize(self, root: Path, **overrides: object) -> Path:
        values = {
            "submission_id": "example-generation-01",
            "title": "Example generation profile",
            "track": "generation",
            "configuration_label": "frontier-lab-a",
            "provenance_level": "attested_alias",
            "taskpack_id": "frontier-model-handoff-v0.1",
            "taskpack_version": "0.1",
            "contributor": "Example Researcher",
            "attestor": "Example Researcher",
            "attestation": "Exact configuration retained privately by the submitter.",
        }
        values.update(overrides)
        output = root / "submission"
        initialize_submission([REPORT], output, **values)
        return output

    def test_initialize_validate_and_bundle(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            submission = self.initialize(root)
            manifest, artifacts = validate_submission(submission)
            self.assertEqual(manifest["configuration"]["provenance_level"], "attested_alias")
            self.assertEqual(len(artifacts), 2)
            first = bundle_submission(submission, root / "submission-1.tar.gz")
            second = bundle_submission(submission, root / "submission-2.tar.gz")
            self.assertEqual(first, second)
            self.assertEqual(
                (root / "submission-1.tar.gz").read_bytes(),
                (root / "submission-2.tar.gz").read_bytes(),
            )

    def test_public_provenance_requires_model_id(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaises(SubmissionError):
                self.initialize(
                    Path(directory),
                    provenance_level="public",
                    attestor=None,
                    attestation=None,
                )

    def test_digest_tampering_is_rejected(self) -> None:
        with TemporaryDirectory() as directory:
            submission = self.initialize(Path(directory))
            summary = submission / "summary.json"
            summary.write_text(summary.read_text() + " ", encoding="utf-8")
            with self.assertRaisesRegex(SubmissionError, "digest mismatch"):
                validate_submission(submission)

    def test_private_denylist_blocks_withheld_identifier(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            submission = self.initialize(root)
            report = next((submission / "evidence").glob("*.json"))
            payload = json.loads(report.read_text())
            payload["functional"]["stdout"] = "PRIVATE-CHECKPOINT-123"
            report.write_text(json.dumps(payload), encoding="utf-8")
            manifest_path = submission / "submission.json"
            manifest = json.loads(manifest_path.read_text())
            import hashlib

            relative = report.relative_to(submission).as_posix()
            manifest["digests"][relative] = hashlib.sha256(report.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            denylist = root / "denylist.txt"
            denylist.write_text("PRIVATE-CHECKPOINT-[0-9]+\n", encoding="utf-8")
            with self.assertRaisesRegex(SubmissionError, "private denylist"):
                validate_submission(submission, denylist=denylist)

    def test_diagnosis_result_is_preserved_as_challenge_evidence(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "diagnosis"
            initialize_submission(
                [DIAGNOSIS_RESULT],
                output,
                submission_id="example-diagnosis-01",
                title="Example diagnosis profile",
                track="diagnosis",
                configuration_label="gpt-5.4",
                provenance_level="public",
                model_id="gpt-5.4",
                taskpack_id="frontier-model-handoff-v0.1",
                taskpack_version="0.1",
                contributor="Example Researcher",
            )
            validate_submission(output)
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual(summary["kind"], "challenge_results")
            self.assertEqual(summary["result_count"], 1)
            self.assertEqual(summary["overall_statuses"], {"fail": 1, "pass": 0})

    def test_challenge_result_must_match_configuration_label(self) -> None:
        with TemporaryDirectory() as directory:
            with self.assertRaisesRegex(SubmissionError, "configuration label"):
                initialize_submission(
                    [DIAGNOSIS_RESULT],
                    Path(directory) / "diagnosis",
                    submission_id="example-diagnosis-01",
                    title="Example diagnosis profile",
                    track="diagnosis",
                    configuration_label="different-model",
                    provenance_level="public",
                    model_id="different-model",
                    taskpack_id="frontier-model-handoff-v0.1",
                    taskpack_version="0.1",
                    contributor="Example Researcher",
                )
