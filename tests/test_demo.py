from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
from unittest import TestCase, skipUnless

from svgap.cli import main
from svgap.demo import DemoError, materialize_demo


HAS_TOOLS = all(shutil.which(tool) for tool in ("yosys", "iverilog", "vvp"))


@skipUnless(HAS_TOOLS, "Yosys and Icarus Verilog are required")
class DemoTests(TestCase):
    def test_demo_rejects_a_file_as_output_directory(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "not-a-directory"
            output.write_text("occupied", encoding="utf-8")
            with self.assertRaisesRegex(DemoError, "not a directory"):
                materialize_demo(output)

    def test_demo_is_a_successful_explanation_of_an_expected_finding(self) -> None:
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = main(["demo"])
        self.assertEqual(code, 0)
        output = stream.getvalue()
        self.assertIn("same functional result", output)
        self.assertIn("safe       pass", output)
        self.assertIn("unsafe     pass", output)
        self.assertIn("REF-RDC-001", output)

    def test_demo_can_preserve_machine_readable_artifacts(self) -> None:
        with TemporaryDirectory() as directory:
            output = Path(directory) / "demo"
            with redirect_stdout(io.StringIO()):
                code = main(["demo", "--output", str(output), "--json"])
            self.assertEqual(code, 0)
            summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["status"], "pass")
            self.assertEqual(summary["safe"]["structural"], "pass")
            self.assertEqual(summary["unsafe"]["structural"], "fail")
            self.assertTrue((output / "safe/build/report.json").is_file())
            self.assertTrue((output / "unsafe/build/report.json").is_file())
