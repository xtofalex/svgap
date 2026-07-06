import base64
import json
from pathlib import Path
import shutil
import sys
from tempfile import TemporaryDirectory
from unittest import TestCase, skipUnless
from unittest.mock import patch

from svgap.resources import taskpack_metadata, taskpack_root
from svgap.study_runner import (
    StudyError,
    evaluate_saved_responses,
    run_quickstart,
    run_study,
    select_study_shape,
)


HAS_TOOLS = all(shutil.which(tool) for tool in ("yosys", "iverilog", "vvp"))


def command_for(text: str) -> str:
    encoded = base64.b64encode(text.encode()).decode()
    return (
        f'{sys.executable} -c "import base64; '
        f'print(base64.b64decode(\'{encoded}\').decode())"'
    )


class TaskpackResourceTests(TestCase):
    def test_reset_release_taskpack_is_discoverable(self) -> None:
        metadata = taskpack_metadata("reset-release-v0.2")
        self.assertEqual(metadata["version"], "0.2")
        self.assertEqual(metadata["smoke_task"], "reset_counter")
        self.assertEqual(len(metadata["tasks"]), 8)
        self.assertTrue(metadata["canonical_digest"].startswith("sha256:"))

    def test_default_shape_is_one_task_one_sample(self) -> None:
        tasks, samples, mode = select_study_shape("reset-release-v0.2")
        self.assertEqual(tasks, ["reset_counter"])
        self.assertEqual(samples, 1)
        self.assertEqual(mode, "smoke")

    def test_full_shape_is_frozen_protocol(self) -> None:
        tasks, samples, mode = select_study_shape("reset-release-v0.2", full=True)
        self.assertEqual(len(tasks), 8)
        self.assertEqual(samples, 3)
        self.assertEqual(mode, "full")

    def test_quickstart_stops_with_doctor_guidance_when_tools_are_missing(self) -> None:
        with TemporaryDirectory() as directory, patch(
            "svgap.study_runner.shutil.which", return_value=None
        ):
            with self.assertRaisesRegex(StudyError, "svgap doctor"):
                run_quickstart(output=Path(directory) / "quickstart")


@skipUnless(HAS_TOOLS, "Yosys and Icarus Verilog are required")
class StudyRunnerTests(TestCase):
    def safe_response(self) -> str:
        return (
            taskpack_root("reset-release-v0.2")
            / "tasks/reset_counter/reference-safe.sv"
        ).read_text(encoding="utf-8")

    def test_smoke_study_writes_profile_and_portable_report(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "study"
            result = run_study(
                "reset-release-v0.2",
                command=command_for(self.safe_response()),
                label="example-model",
                interface_label="test-harness",
                output=output,
            )
            self.assertEqual(result["report_count"], 1)
            self.assertEqual(result["functional_pass"], 1)
            self.assertEqual(result["gap_members"], 0)
            self.assertTrue((output / "study-summary.json").is_file())
            self.assertTrue((output / "evidence-profile.html").is_file())
            report_path = next(output.glob("*/*/report.json"))
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertFalse(report["manifest"].startswith("/"))
            self.assertNotIn("/Users/", report_path.read_text(encoding="utf-8"))
            self.assertNotIn("/home/", report_path.read_text(encoding="utf-8"))

    def test_all_generation_failures_point_to_diagnostics(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "failed-study"
            command = f'{sys.executable} -c "import sys; sys.exit(7)"'
            with self.assertRaisesRegex(StudyError, "inspect .*failures.json"):
                run_study(
                    "reset-release-v0.2",
                    command=command,
                    label="broken-adapter",
                    interface_label="test-harness",
                    output=output,
                )
            failures = json.loads((output / "failures.json").read_text())
            self.assertEqual(len(failures["failures"]), 1)
            self.assertIn("exited 7 with no stderr", failures["failures"][0])

    def test_quickstart_is_explicit_fixture_and_writes_legible_profile(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "quickstart"
            result = run_quickstart(output=output)
            self.assertEqual(result["mode"], "quickstart")
            self.assertTrue(result["fixture"])
            self.assertEqual(result["functional_pass"], 1)
            self.assertEqual(result["gap_members"], 1)
            self.assertTrue(Path(result["first_report"]).is_file())
            profile = Path(result["profile"]).read_text(encoding="utf-8")
            self.assertIn("What this result means", profile)
            self.assertIn("What evidence to add next", profile)
            generation = next(output.glob("*/*/generation.json"))
            self.assertTrue(json.loads(generation.read_text())["generation_config"]["fixture"])
            absolute_output = str(output.resolve())
            for artifact in output.rglob("*.json"):
                self.assertNotIn(absolute_output, artifact.read_text(encoding="utf-8"))

    def test_generate_then_evaluate_saved(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            generated = root / "generated"
            result = run_study(
                "reset-release-v0.2",
                command=command_for(self.safe_response()),
                label="example-model",
                interface_label="test-harness",
                output=generated,
                generate_only=True,
            )
            self.assertEqual(result["responses"], 1)
            evaluated = evaluate_saved_responses(
                "reset-release-v0.2",
                responses=generated / "_responses",
                output=root / "evaluated",
            )
            self.assertEqual(evaluated["report_count"], 1)
